import { useEffect, useRef, useState } from 'react';
import { LogIn, ThumbsUp, Tool, TrendingUp } from 'react-feather';
import { NavLink } from 'react-router-dom';
import { ReactComponent as Logo } from '../images/logo.svg';

const Navbar = () => {

    const [state, setState] = useState('');
    const mediaQ = useRef(window.matchMedia('(min-width: 46em)'));

    const checkMediaQ = () => {
        if (mediaQ.current.matches) setState('');
        else setState('mobile');
    };

    useEffect(() => {
        checkMediaQ();

        const currentMediaQ = mediaQ.current;

        currentMediaQ.addEventListener('change', checkMediaQ);

        return () => {
            currentMediaQ.removeEventListener('change', checkMediaQ);
        }
    }, []);

    return (
        <header className="main-nav">
            <div className="title-wrapper">
                <Logo />
                <p className="title">Dynasty Tools</p>
            </div>

            <nav>
                <ul>
                    <li className="link">
                        <NavLink to="/vote">
                            <ThumbsUp />
                            { state !== 'mobile' && 'Vote' }
                        </NavLink>
                    </li>
                    <li className="link">
                        <NavLink to="/rankings">
                            <TrendingUp />
                            { state !== 'mobile' && 'Rankings' }
                        </NavLink>
                    </li>
                    <li className="link">
                        <NavLink to="/calculator">
                            <Tool />
                            { state !== 'mobile' && 'Calculator' }
                        </NavLink>
                    </li>
                </ul>
            </nav>

            <button className="login-btn">
                <LogIn />
                { state !== 'mobile' && 'Login' }
            </button>
        </header>
    )
}

export default Navbar;