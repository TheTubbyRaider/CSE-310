using System;

namespace PersonalBudgetManager
{
    class Program
    {
        static void Main(string[] args)
        {
            BudgetManager budgetManager = new BudgetManager();
            budgetManager.LoadData();

            while (true)
            {
                Console.WriteLine("=== Personal Budget Management Application ===");
                Console.WriteLine("1. Add Income");
                Console.WriteLine("2. Add Expense");
                Console.WriteLine("3. Generate Monthly Report");
                Console.WriteLine("4. Exit");
                Console.Write("Choose an option: ");
                string choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        budgetManager.AddTransaction(TransactionType.Income);
                        break;
                    case "2":
                        budgetManager.AddTransaction(TransactionType.Expense);
                        break;
                    case "3":
                        budgetManager.GenerateMonthlyReport();
                        break;
                    case "4":
                        budgetManager.SaveData();
                        Console.WriteLine("Exiting the application. Goodbye!");
                        return;
                    default:
                        Console.WriteLine("Invalid option. Please try again.");
                        break;
                }
                Console.WriteLine();
            }
        }
    }
}
