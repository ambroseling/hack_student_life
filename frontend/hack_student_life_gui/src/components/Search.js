import { Row,Input } from "reactstrap";
import { Fragment } from "react";
const Search = () => {
    return <Fragment>
        <Row>
            <h4>What are you looking for?</h4>
        </Row>
            <Input
                type="text"
                placeholder="Search"
                className="search-input"
            />
        </Fragment>
}

export default Search;