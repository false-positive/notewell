import React from 'react';
import { Link } from 'react-router-dom';

/**
 * A thin wrapper around react-router-dom's `Link`
 * that takes `href` instead of `to`.
 *
 * Typically passed to MUI Buttons as the `LinkComponent`.
 */
const HrefRouterLink = React.forwardRef<HTMLAnchorElement, { href: string }>(
    ({ href, children, ...props }, ref) => (
        <Link ref={ref} to={href} {...props}>
            {children}
        </Link>
    )
);

export default HrefRouterLink;
