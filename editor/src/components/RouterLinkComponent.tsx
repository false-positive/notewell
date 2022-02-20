import React from 'react';
import { Link } from 'react-router-dom';

const RouterLinkComponent = React.forwardRef<
    HTMLAnchorElement,
    { href: string; className: string }
>(({ href, children, ...props }, ref) => (
    <Link ref={ref} to={href} {...props}>
        {children}
    </Link>
));

export default RouterLinkComponent;
