const express = require('express');
const mysql = require('mysql');

const app = express();

const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "tourism"
})

// Get all destinations
app.get('/destination', (req, res) => {
    const sql = 'SELECT * FROM destinations';
    db.query(sql, (err, result) => {
        if (err) {
            console.error('Error fetching destinations:', err);
            res.status(500).json({ error: 'Internal server error' });
            return;
        }
        res.json(result);
    });
});

// Get destination by id
app.get('/destination/:DestinationID', (req, res) => {
    const destinationId = parseInt(req.params.DestinationID);
    db.query('SELECT * FROM destinations WHERE DestinationID = ?', [destinationId], (err, result) => {
        if (err) {
            console.error('Error fetching destination:', err);
            res.status(500).json({ error: 'Internal server error' });
            return;
        }
        if (result.length > 0) {
            res.json(result[0]);
        } else {
            res.status(404).json({ error: 'Destination not found' });
        }
    });
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

// Close database connection when the app is terminated
process.on('SIGINT', () => {
    console.log('Closing MySQL connection...');
    db.end((err) => {
        if (err) {
            console.error('Error closing MySQL connection:', err);
        } else {
            console.log('MySQL connection closed');
        }
        process.exit();
    });
});
