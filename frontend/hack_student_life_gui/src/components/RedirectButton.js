import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button } from "reactstrap";

const RedirectButton = ({ icon, link }) => {
    return (
        <FontAwesomeIcon className="redirect-button" icon={icon} href={link}/>
    )
}

export default RedirectButton;