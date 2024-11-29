import { Row,Input, InputGroupText, InputGroup } from "reactstrap";
import { Fragment } from "react";
const Search = () => {
    return <Fragment>
                <Input
                    type="text"
                    placeholder="What are you looking for?"
                    className="search-input"
                />
        </Fragment>
}

export default Search;