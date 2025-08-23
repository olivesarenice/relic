document.addEventListener('DOMContentLoaded', () => {
    const authForm = document.getElementById('authForm');
    const clientIdInput = document.getElementById('clientId');
    const apiKeyInput = document.getElementById('apiKey');
    const sendDataForm = document.getElementById('sendDataForm');
    const responseMessage = document.getElementById('responseMessage');
    const deviceInfoInput = document.getElementById('deviceInfo');
    const setupSection = document.getElementById('setup-section');
    const quicklogSection = document.getElementById('quicklog-section');
    const goToSetupButton = document.getElementById('goToSetupButton');
    const setupResponseMessage = document.getElementById('setupResponseMessage');
    const logSavedAnimation = document.getElementById('logSavedAnimation'); // Get the animation element
    let userLocation = null; // Variable to store user's location

    // Function to check if all required credentials are set
    const areCredentialsSet = () => {
        return localStorage.getItem('clientId') &&
            localStorage.getItem('apiKey') &&
            localStorage.getItem('deviceInfo');
    };

    // Function to show/hide sections
    const showSection = (sectionToShow) => {
        if (sectionToShow === 'setup') {
            setupSection.style.display = 'block';
            quicklogSection.style.display = 'none';
        } else {
            setupSection.style.display = 'none';
            quicklogSection.style.display = 'block';
            getLocation(); // Fetch location when quicklog section is shown
        }
    };

    // Function to get user's location
    const getLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    userLocation = {
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    };
                },
                (error) => {
                    console.error('Error getting location:', error);
                    userLocation = null;
                }
            );
        } else {
            console.warn('Geolocation not supported by this browser.');
            userLocation = null;
        }
    };

    // Function to save credentials and device info to local storage
    const saveCredentials = () => {
        localStorage.setItem('clientId', clientIdInput.value);
        localStorage.setItem('apiKey', apiKeyInput.value);
        localStorage.setItem('deviceInfo', deviceInfoInput.value);
        setupResponseMessage.textContent = 'Credentials and Device Info saved successfully!';
        setupResponseMessage.style.color = 'green';
        showSection('quicklog'); // After saving, go to quick log page
    };

    // Function to load credentials and device info from local storage
    const loadCredentials = () => {
        const savedClientId = localStorage.getItem('clientId');
        const savedApiKey = localStorage.getItem('apiKey');
        const savedDeviceInfo = localStorage.getItem('deviceInfo');

        if (savedClientId) {
            clientIdInput.value = savedClientId;
        }
        if (savedApiKey) {
            apiKeyInput.value = savedApiKey;
        }
        if (savedDeviceInfo) {
            deviceInfoInput.value = savedDeviceInfo;
        }
    };

    // Load credentials and decide which section to show when the page loads
    loadCredentials();
    if (areCredentialsSet()) {
        showSection('quicklog');
    } else {
        showSection('setup');
    }

    // Handle auth form submission
    authForm.addEventListener('submit', (e) => {
        e.preventDefault();
        saveCredentials();
    });

    // Handle "Go to Setup" button click
    goToSetupButton.addEventListener('click', () => {
        showSection('setup');
    });

    // Handle Ctrl-Enter to send message
    const dataJsonTextarea = document.getElementById('dataJson');

    // Function to auto-expand textarea
    const autoExpandTextarea = () => {
        dataJsonTextarea.style.height = 'auto';
        dataJsonTextarea.style.height = dataJsonTextarea.scrollHeight + 'px';
    };

    // Auto-expand on input
    dataJsonTextarea.addEventListener('input', autoExpandTextarea);

    // Handle Ctrl-Enter to send message
    dataJsonTextarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { // Ctrl+Enter for Windows/Linux, Cmd+Enter for Mac
            e.preventDefault(); // Prevent new line
            sendDataForm.dispatchEvent(new Event('submit')); // Trigger form submission
        }
    });

    // Handle send data form submission
    sendDataForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const clientId = localStorage.getItem('clientId');
        const apiKey = localStorage.getItem('apiKey');

        if (!clientId || !apiKey) {
            responseMessage.textContent = 'Please save your Client ID and API Key first.';
            responseMessage.style.color = 'red';
            return;
        }

        const userFormInput = document.getElementById('dataJson').value;
        const deviceInfo = deviceInfoInput.value; // Get the device info from the input field

        const dataToSend = {
            "collector": "webapp",
            "source_type": "quicklog",
            "data_json": {
                "device": deviceInfo, // Use the user-provided device info
                "location": userLocation, // Include location data
                "form_text": userFormInput
            }
        };

        try {
            const response = await fetch('http://localhost:8000/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CLIENT-ID': clientId,
                    'X-API-KEY': apiKey
                },
                body: JSON.stringify(dataToSend)
            });

            if (response.ok) {
                const result = await response.json();
                logSavedAnimation.classList.add('show');
                setTimeout(() => {
                    logSavedAnimation.classList.remove('show');
                }, 500); // Show for 0.5 seconds
                responseMessage.textContent = ''; // Clear previous text message
            } else {
                const errorText = await response.text();
                responseMessage.textContent = `Error sending data: ${response.status} - ${errorText}`;
                responseMessage.style.color = 'red';
            }
        } catch (error) {
            responseMessage.textContent = `Network error: ${error.message}`;
            responseMessage.style.color = 'red';
        }
    });
});
