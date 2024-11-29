import React from 'react';
import { Button } from 'reactstrap';
import fetchImportEvents from '../api/importEvents';

const Retrieve = () => {
    const handleImport = async () => {
        try {
            const response = await fetchImportEvents.fetchImportEvents();
            console.log('Import successful:', response);
        } catch (error) {
            console.error('Error importing events:', error);
        }
    };

    return (
        <Button 
            color="primary"
            onClick={handleImport}
            className="mb-3"
        >
            Import Events
        </Button>
    );
};

export default Retrieve;
