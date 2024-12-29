const URL = 'http://127.0.0.1:5000/api/' // adicionar .env

async function loadACStatus() {
    try {
        const response = await fetch(URL + 'ac-status');
        if (!response.ok) {
            throw new Error('Erro ao buscar o status do ar-condicionado');
        }
        const acStatus = await response.json();
        return acStatus;
    } catch (error) {
        console.error(error.message);
        return {
            isOn: true,
            temperature: 25,
            error: true,
        };
    }
}

async function increaseTemperature() {
    try {
        const response = await fetch(URL + 'ac-increase');
        if (!response.ok) {
            throw new Error('Erro increase');
        }
        const acStatus = await response.json();
        return acStatus;
    } catch (error) {
        console.error(error.message);
        return {
            isOn: true,
            temperature: 26,
            error: true,
        };
    }
}

async function decreaseTemperature() {
    try {
        const response = await fetch(URL + 'ac-decrease');
        if (!response.ok) {
            throw new Error('Erro decrease');
        }
        const acStatus = await response.json();
        return acStatus;
    } catch (error) {
        console.error(error.message);
        return {
            isOn: true,
            temperature: 24,
            error: true,
        };
    }
}

async function toggleAC() {
    try {
        const response = await fetch(URL + 'ac-toggle');
        if (!response.ok) {
            throw new Error('Erro decrease');
        }
        const acStatus = await response.json();
        return acStatus;
    } catch (error) {
        console.error(error.message);
        return {
            isOn: true,
            temperature: 24,
            error: true,
        };
    }
}

async function loadAmbientTemperature() {
    try {
        const response = await fetch(URL + 'sensor-temperature');
        if (!response.ok) {
            throw new Error('Erro sensor temperature');
        }
        const temperatureInfo = await response.json();
        return temperatureInfo;
    } catch (error) {
        console.error(error.message);
        return {
            temperature: 24,
            error: true,
        };
    }
}

async function changeTVColor(color) {
    try {
        const response = await fetch(URL + 'change-color', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', 
            },
            body: JSON.stringify({ color: color }), 
        });

        if (!response.ok) {
            throw new Error('Erro ao mudar a cor da TV');
        }

        const data = await response.json();
        return data; 
    } catch (error) {
        console.error('Erro:', error.message);
        return { error: error.message }; 
    }
}