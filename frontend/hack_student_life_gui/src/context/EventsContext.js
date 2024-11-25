import React, { createContext, useState, useEffect, useContext } from "react";
import fetchAllEvents from "../api/fetchAllEvents";
const EventsContext = createContext();

export const EventsProvider = ({ children }) => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const response = await fetchAllEvents();
                console.log(response);
                setEvents(response);
                setLoading(false);
            } catch (error) {
                setError(error);
                setLoading(false);
            }
            finally {
                setLoading(false);
            }
        };
        fetchEvents();
    }, []);

    return (
        <EventsContext.Provider value={{ events, loading, error }}>
            {children}
        </EventsContext.Provider>
    );
}

export const useEvents = () => useContext(EventsContext);