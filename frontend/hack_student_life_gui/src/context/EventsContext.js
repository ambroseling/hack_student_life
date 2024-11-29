import React, { createContext, useState, useEffect, useContext } from "react";
const EventsContext = createContext();

export const EventsProvider = ({ children }) => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchEvents = async (search = '') => {
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:8000/api/get-events${search ? `?search=${search}` : ''}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setEvents(data);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching events:', error);
            setError(error);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchEvents();
    }, []);

    return (
        <EventsContext.Provider value={{ events, loading, error, fetchEvents }}>
            {children}
        </EventsContext.Provider>
    );
}

export const useEvents = () => useContext(EventsContext);