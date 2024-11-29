import React from 'react';
import { Button } from 'reactstrap';

const FilterButton = ({ tag, isToggled, onToggle }) => {
    return (
        <Button 
            color = "light" 
            onClick={() => onToggle(tag)} 
            outline={!isToggled} 
            className="mb-3 mr-3" 
            size="sm"
        >
            {tag}
        </Button>
    );
};

export default FilterButton;

