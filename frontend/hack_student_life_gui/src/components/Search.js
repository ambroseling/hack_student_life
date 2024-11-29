<<<<<<< HEAD
import { Row, Input } from "reactstrap";
=======
import { Row,Input, InputGroupText, InputGroup } from "reactstrap";
>>>>>>> origin/ui
import { Fragment } from "react";

const Search = ({ onSearchChange }) => {
    return <Fragment>
<<<<<<< HEAD
        <Row>
            <h4>What are you looking for?</h4>
        </Row>
        <Input
            type="text"
            placeholder="Search"
            className="search-input"
            onChange={(e) => onSearchChange(e.target.value)}
        />
    </Fragment>
=======
                <Input
                    type="text"
                    placeholder="What are you looking for?"
                    className="search-input"
                />
        </Fragment>
>>>>>>> origin/ui
}

export default Search;