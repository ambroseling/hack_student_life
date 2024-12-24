import { useState, Fragment } from "react";
import { Input } from "reactstrap";

const Search = ({ onSearch }) => {
    const [searchValue, setSearchValue] = useState("");

    const handleInputChange = (e) => {
        setSearchValue(e.target.value);
    };

    const handleSearch = () => {
        if (onSearch) {
            onSearch(searchValue);
        }
    };

    return (
        <Fragment>
            <Input
                className="search-input-container"
                type="text"
                placeholder="What are you looking for?"
                value={searchValue}
                onChange={handleInputChange}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
        </Fragment>
    );
};

export default Search;
