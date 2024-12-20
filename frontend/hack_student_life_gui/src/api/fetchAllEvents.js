import axios from "axios";

const fetchAllEvents = async () => {
    try {
        console.log("before fetchAllEvents!!!");
        const response = await axios.get(`localhost:8000/api/get-events`);
        console.log("fetchAllEvents!!!");
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error fetching events:", error);
        throw error;
    }
};


export default {
    fetchAllEvents
};