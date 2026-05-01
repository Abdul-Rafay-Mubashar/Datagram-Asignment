# 📊 Data Scraping & MySQL Integration Assignment

---

## 📌 Overview

This project demonstrates a simple **data scraping pipeline and database integration workflow** using Python and MySQL.

It collects data using a scraping API, processes it in Python, and stores it into a **MySQL database table** for further analysis.

The goal of this assignment is to understand:

* Web scraping basics
* API usage
* Database creation and insertion
* Python-to-MySQL integration

---

## 🧠 Core Workflow

1. Data is fetched using a scraping API
2. Python processes and structures the data
3. Data is inserted into MySQL database
4. Results are verified using SQL queries

---

## ⚙️ Setup Instructions

### 🔹 1. Scraper API Setup

* Create an account on Scraper API
* Get your API key
* Replace it in `Datagram_Assignment.py` (Line 14)

---

### 🔹 2. Python Dependencies

Install required libraries:

```bash id="z2lq7k"
pip install requests beautifulsoup4 sqlalchemy pymysql pandas
```

---

## 🗄️ MySQL Setup

Run the following queries in **MySQL Workbench (step by step)**:

```sql id="kq8p3d"
create database mydb;

use mydb;

CREATE TABLE db_table (
    Name VARCHAR(255),
    Brand VARCHAR(255),
    Price VARCHAR(255),
    Product_Url VARCHAR(255),
    Img_Url VARCHAR(255)
);
```

---

## 🐍 JSON to MySQL Script Setup

In `Json_To_MySQL.py`:

* Install dependencies:

  * sqlalchemy
  * pymysql
  * pandas

* Configure:

  * MySQL password
  * Port number

---

## 📊 Verify Data

After running scripts, execute:

```sql id="m1x9aa"
select * from db_table;
```

This will display all scraped and stored records.

---

## 💡 What This Project Teaches

* Web scraping using APIs
* Working with structured data
* Database schema creation
* Python + MySQL integration
* End-to-end data pipeline flow

---

## 📌 Summary

This assignment demonstrates a basic **data pipeline system** where data is:
**Scraped → Processed → Stored → Queried**

It builds foundational understanding of **real-world data engineering workflows**.

---
