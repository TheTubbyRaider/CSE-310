using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json; // Install Newtonsoft.Json via NuGet

namespace PersonalBudgetManager
{
    public class BudgetManager
    {
        private List<Transaction> Transactions { get; set; }
        private readonly string filePath = "budgetData.json";

        public BudgetManager()
        {
            Transactions = new List<Transaction>();
        }

        public void AddTransaction(TransactionType type)
        {
            decimal amount = 0;
            while (true)
            {
                Console.Write("Enter amount: ");
                if (decimal.TryParse(Console.ReadLine(), out amount) && amount > 0)
                {
                    break;
                }
                Console.WriteLine("Invalid input. Please enter a positive number.");
            }

            Console.Write("Enter category: ");
            string category = Console.ReadLine();

            Transactions.Add(new Transaction
            {
                Date = DateTime.Now,
                Amount = amount,
                Category = category,
                Type = type
            });

            Console.WriteLine("Transaction added successfully.");
        }

        public void GenerateMonthlyReport()
        {
            Console.WriteLine("\n=== Monthly Report ===");
            decimal totalIncome = 0;
            decimal totalExpense = 0;

            foreach (var transaction in Transactions)
            {
                if (transaction.Type == TransactionType.Income)
                {
                    totalIncome += transaction.Amount;
                }
                else
                {
                    totalExpense += transaction.Amount;
                }
            }

            Console.WriteLine($"Total Income: {totalIncome:C}");
            Console.WriteLine($"Total Expense: {totalExpense:C}");
            Console.WriteLine($"Net Savings: {totalIncome - totalExpense:C}\n");
        }

        public void LoadData()
        {
            if (File.Exists(filePath))
            {
                var jsonData = File.ReadAllText(filePath);
                Transactions = JsonConvert.DeserializeObject<List<Transaction>>(jsonData);
                Console.WriteLine("Data loaded successfully.");
            }
            else
            {
                Console.WriteLine("No previous data found. Starting fresh.");
            }
        }

        public void SaveData()
        {
            var jsonData = JsonConvert.SerializeObject(Transactions, Formatting.Indented);
            File.WriteAllText(filePath, jsonData);
            Console.WriteLine("Data saved successfully.");
        }
    }
}
