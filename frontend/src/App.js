import React, { useState, useEffect } from 'react';
import { useTable } from 'react-table';
import './App.css'; // Make sure to import the CSS file

function App() {
    const [data, setData] = useState([]);
    const [loggedIn, setLoggedIn] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    useEffect(() => {
        if (loggedIn) fetchData();
    }, [loggedIn]);

    const fetchData = async () => {
        try {
            const response = await fetch(`/get_files?username=${username}`);
            const result = await response.json();
            console.log(result.files); // Debugging purpose
            setData(result.files);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        const loginPayload = { username, password };
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(loginPayload)
            });
            const result = await response.json();
            if (response.ok) {
                setLoggedIn(true);
            } else {
                alert(result.message);
            }
        } catch (error) {
            console.error('Login failed:', error);
            alert('Login failed due to a network or server error.');
        }
    };

    const handleDownloadFile = (downloadId) => {
        const fileName = `${downloadId}.txt`;
        const fileUrl = `${process.env.PUBLIC_URL}/files/${fileName}`;
        const link = document.createElement('a');
        link.href = fileUrl;
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    const columns = React.useMemo(() => [
        { Header: 'ID', accessor: 'id' },
        { Header: 'User', accessor: 'user' },
        { Header: 'Description', accessor: 'description' },
    ], []);

    const tableInstance = useTable({
        columns,
        data: data || []
    });

    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
    } = tableInstance;

    if (!loggedIn) {
        return (
            <div className="login-container">
                <h2>Login to Electronic Health Records (EHR)</h2>
                <form onSubmit={handleLogin} className="login-form">
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    />
                    <button type="submit">Log In</button>
                </form>
            </div>
        );
    }

    return (
        <div>
            <div className="header">
                <h1>Electronic Health Records (EHR)</h1>
            </div>
            <div>
                <table {...getTableProps()}>
                    <thead>
                    {headerGroups.map(headerGroup => (
                        <tr {...headerGroup.getHeaderGroupProps()}>
                            {headerGroup.headers.map(column => (
                                <th {...column.getHeaderProps()}>{column.render('Header')}</th>
                            ))}
                            <th>Actions</th>
                        </tr>
                    ))}
                    </thead>
                    <tbody {...getTableBodyProps()}>
                    {rows.map(row => {
                        prepareRow(row);
                        return (
                            <tr {...row.getRowProps()}>
                                {row.cells.map(cell => (
                                    <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                                ))}
                                <td>
                                    <button onClick={() => handleDownloadFile(row.cells[0].value)}>
                                        Download
                                    </button>
                                </td>
                            </tr>
                        );
                    })}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default App;
