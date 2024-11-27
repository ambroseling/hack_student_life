import axios from "axios";

const fetchAllEvents = async () => {
    try {
        const response = await axios.get("http://localhost:8000/api/events");
        return response.data;
    } catch (error) {
        console.error("Error fetching events:", error);
        throw error;
    }
};

export default fetchAllEvents