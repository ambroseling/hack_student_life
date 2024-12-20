import axios from "axios";
const fetchImportEvents = async () => {
    try {
        const response = await axios.get(`localhost:8000/api/import-events`);
        return response.data;
    } catch (error) {
        console.error("Error fetching events:", error);
        throw error;
    }
};

export default {
    fetchImportEvents
};