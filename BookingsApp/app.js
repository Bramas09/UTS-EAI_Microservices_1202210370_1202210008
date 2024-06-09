const express = require("express");
const mysql = require("mysql");

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "",
  database: "tourism",
});

// Connect to database
db.connect((err) => {
  if (err) {
    console.error("Error connecting to database:", err);
    return;
  }
  console.log("Connected to MySQL database");
});

// Create a new customer
app.post("/create-customer", (req, res) => {
  const { CustomerID, CustomerName, NIK, Email, Address } = req.body;

  if (!CustomerID || !CustomerName || !NIK || !Email || !Address) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  const customerInsertSql =
    "INSERT INTO customer (CustomerID, CustomerName, NIK, Email, Address) VALUES (?, ?, ?, ?, ?)";

  db.query(
    customerInsertSql,
    [CustomerID, CustomerName, NIK, Email, Address],
    (err, result) => {
      if (err) {
        console.error("Error inserting customer:", err);
        return res.status(500).json({ error: "Internal server error" });
      }
      res.json({ message: "Customer created successfully" });
    }
  );
});

// Create a new booking
app.post("/create-booking", (req, res) => {
  const { BookingID, CustomerID, DestinationID } = req.body;

  if (!BookingID || !CustomerID || !DestinationID) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  const bookingInsertSql =
    "INSERT INTO bookings (BookingID, CustomerID, DestinationID) VALUES (?, ?, ?)";

  db.query(
    bookingInsertSql,
    [BookingID, CustomerID, DestinationID],
    (err, result) => {
      if (err) {
        console.error("Error inserting booking:", err);
        return res.status(500).json({ error: "Internal server error" });
      }
      res.json({ message: "Booking created successfully", BookingID });
    }
  );
});


// Get all bookings
app.get("/show-booking", (req, res) => {
  const sql = `
    SELECT bookings.BookingID, customer.CustomerName, customer.Email, destinations.DestinationName, destinations.Location, destinations.Price
    FROM bookings 
    JOIN customer ON bookings.CustomerID = customer.CustomerID
    JOIN destinations ON bookings.DestinationID = destinations.DestinationID
    ORDER BY bookings.BookingID ASC`;
  db.query(sql, (err, result) => {
    if (err) {
      console.error("Error fetching bookings:", err);
      return res.status(500).json({ error: "Internal server error" });
    }
    res.json(result);
  });
});

// Get booking by ID
app.get("/show-booking/:BookingID", (req, res) => {
  const BookingID = parseInt(req.params.BookingID);
  db.query(
    "SELECT bookings.BookingID, customer.CustomerID, customer.CustomerName, customer.NIK, customer.Email, customer.Address, destinations.DestinationID, destinations.DestinationName, destinations.Location, destinations.Rating, destinations.Viewers, destinations.Price FROM bookings JOIN customer ON bookings.CustomerID = customer.CustomerID JOIN destinations ON bookings.DestinationID = destinations.DestinationID WHERE bookings.BookingID = ?",
    [BookingID],
    (err, result) => {
      if (err) {
        console.error("Error fetching booking:", err);
        return res.status(500).json({ error: "Internal server error" });
      }
      if (result.length > 0) {
        res.json(result[0]);
      } else {
        res.status(404).json({ error: "Booking not found" });
      }
    }
  );
});

// Update booking by ID
app.put("/update-booking/:BookingID", (req, res) => {
  const BookingID = parseInt(req.params.BookingID);
  const {
    CustomerID,
    CustomerName,
    NIK,
    Email,
    Address,
    DestinationID,
    DestinationName,
    Location,
    Rating,
    Viewers,
    Price,
  } = req.body;

  if (
    !CustomerID ||
    !CustomerName ||
    !NIK ||
    !Email ||
    !Address ||
    !DestinationID ||
    !DestinationName ||
    !Location ||
    !Rating ||
    !Viewers ||
    !Price
  ) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  const customerUpdateSql =
    "UPDATE customer SET CustomerName = ?, NIK = ?, Email = ?, Address = ? WHERE CustomerID = ?";
  const destinationUpdateSql =
    "UPDATE destinations SET DestinationName = ?, Location = ?, Rating = ?, Viewers = ?, Price = ? WHERE DestinationID = ?";
  const bookingUpdateSql =
    "UPDATE bookings SET CustomerID = ?, DestinationID = ? WHERE BookingID = ?";

  db.beginTransaction((err) => {
    if (err) {
      console.error("Error starting transaction:", err);
      return res.status(500).json({ error: "Internal server error" });
    }

    db.query(
      customerUpdateSql,
      [CustomerName, NIK, Email, Address, CustomerID],
      (err) => {
        if (err) {
          return db.rollback(() => {
            console.error("Error updating customer:", err);
            res.status(500).json({ error: "Internal server error" });
          });
        }

        db.query(
          destinationUpdateSql,
          [DestinationName, Location, Rating, Viewers, Price, DestinationID],
          (err) => {
            if (err) {
              return db.rollback(() => {
                console.error("Error updating destination:", err);
                res.status(500).json({ error: "Internal server error" });
              });
            }

            db.query(
              bookingUpdateSql,
              [CustomerID, DestinationID, BookingID],
              (err) => {
                if (err) {
                  return db.rollback(() => {
                    console.error("Error updating booking:", err);
                    res.status(500).json({ error: "Internal server error" });
                  });
                }

                db.commit((err) => {
                  if (err) {
                    return db.rollback(() => {
                      console.error("Error committing transaction:", err);
                      res.status(500).json({ error: "Internal server error" });
                    });
                  }

                  res.json({
                    message: "Booking updated successfully",
                    BookingID,
                  });
                });
              }
            );
          }
        );
      }
    );
  });
});

// Delete booking by ID
app.delete("/delete-booking/:BookingID", (req, res) => {
  const BookingID = parseInt(req.params.BookingID);
  const sql = "DELETE FROM bookings WHERE BookingID=?";
  db.query(sql, [BookingID], (err, result) => {
    if (err) {
      console.error("Error deleting booking:", err);
      res.status(500).json({ error: "Internal server error" });
      return;
    }
    res.json({ message: "Booking deleted successfully", BookingID });
  });
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// Close database connection when the app is terminated
process.on("SIGINT", () => {
  console.log("Closing MySQL connection...");
  db.end((err) => {
    if (err) {
      console.error("Error closing MySQL connection:", err);
    } else {
      console.log("MySQL connection closed");
    }
    process.exit();
  });
});
