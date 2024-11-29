import React from 'react';
import { useState, Fragment, useEffect } from "react";
import { Dropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';

function SortDropDown({ sortOption, setSortOption }) {
    const [dropdownOpen, setDropdownOpen] = useState(false);

    const toggle = () => setDropdownOpen(!dropdownOpen);

    return (
        <Dropdown isOpen={dropdownOpen} toggle={toggle} size = "sm">
            <DropdownToggle caret>
                Sort By Date
            </DropdownToggle>
            <DropdownMenu>
                <DropdownItem onClick={() => setSortOption('asc')}>Ascending</DropdownItem>
                <DropdownItem onClick={() => setSortOption('desc')}>Descending</DropdownItem>
            </DropdownMenu>
        </Dropdown>
    );
}

export default SortDropDown;
