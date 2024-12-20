import React from 'react';

const NavBar = () => {
    return (
        <div style={{ 
            backgroundColor: '#f8f9fa',
            padding: '1rem',
            borderRadius: '15px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
            <nav style={{
                display: 'flex',
                justifyContent: 'space-around',
                alignItems: 'center'
            }}>
                <a href="/" style={{
                    textDecoration: 'none',
                    color: '#333',
                    fontWeight: 'bold'
                }}>Home</a>
                <a href="/events" style={{
                    textDecoration: 'none', 
                    color: '#333',
                    fontWeight: 'bold'
                }}>Events</a>
                <a href="/profile" style={{
                    textDecoration: 'none',
                    color: '#333',
                    fontWeight: 'bold'
                }}>Profile</a>
                <a href="/settings" style={{
                    textDecoration: 'none',
                    color: '#333',
                    fontWeight: 'bold'
                }}>Settings</a>
            </nav>
                    </div>
    );
};

export default NavBar;