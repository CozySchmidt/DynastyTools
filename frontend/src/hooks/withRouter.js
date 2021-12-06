import { useLocation } from "react-router"

export const withRouter = (Child) => {
    const Wrapper = (props) => {
        const location = useLocation();

        return <Child {...props} location={location} />
    }

    return Wrapper;
}