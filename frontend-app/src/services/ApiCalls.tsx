const axios = require('axios')

base_URL = 'http://127.0.0.1:8000'

export const getRadarsList = async () => {
    const response = await axios.get(`${base_URL}/radars_list`);
    return response.data;
};

export const getRadarById = async () => {
    const response = await axios.get(`${base_URL}/radar/${id}`);
    return response.data
};