import React, { useState } from 'react';
import { Button } from 'reactstrap';

const FilterButton = ({ tag }) => {
    const [isToggled, setIsToggled] = useState(false);

    const handleToggle = () => {
        setIsToggled(!isToggled);
    };

    return (
        <Button color= 'primary' onClick={handleToggle} outline = {isToggled ? false : true}  className="mb-3 mr-3" size="sm">
            {tag}
        </Button>
    );
};

export default FilterButton;
