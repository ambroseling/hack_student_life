import { Badge } from "reactstrap";

const Tags = ({ tag }) => {
    switch (tag.toLowerCase()) {
        // Career & Professional
        case "career":
        case "professional":
        case "networking":
        case "education":
            return <Badge className="gradient-badge-1 mr-2">{tag}</Badge>;
        
        // Social & Entertainment
        case "social":
        case "entertainment":
        case "games":
        case "music":
            return <Badge className="gradient-badge-2 mr-2">{tag}</Badge>;
        
        // Academic & Research
        case "academic":
        case "research":
        case "educational":
        case "workshop":
            return <Badge className="gradient-badge-3 mr-2">{tag}</Badge>;
        
        // Health & Wellness
        case "wellness":
        case "fitness":
        case "health":
            return <Badge className="gradient-badge-4 mr-2">{tag}</Badge>;
        
        // Food & Culture
        case "food":
        case "cultural":
            return <Badge className="gradient-badge-5 mr-2">{tag}</Badge>;
        
        // Tech & Competition
        case "tech":
        case "competition":
        case "coding":
            return <Badge className="gradient-badge-6 mr-2">{tag}</Badge>;
        
        // Sustainability
        case "sustainability":
            return <Badge className="gradient-badge-7 mr-2">{tag}</Badge>;
        
        // Study
        case "study":
            return <Badge className="gradient-badge-8 mr-2">{tag}</Badge>;
        
        // Default case for any unmatched tags
        default:
            return <Badge className="gradient-badge mr-2">{tag}</Badge>;
    }
}

export default Tags;