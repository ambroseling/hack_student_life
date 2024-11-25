import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button } from "reactstrap";

const RedirectButton = ({ icon, link }) => {
    return (
        <Button className="redirect-button" href={link} style={{backgroundColor: '#ffffff'}}>
            <FontAwesomeIcon icon={icon} style={{color: '#828282'}} />
        </Button>
    )
}

export default RedirectButton;