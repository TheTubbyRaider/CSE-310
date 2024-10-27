using System;

namespace PersonalBudgetManager
{
    public enum TransactionType { Income, Expense }

    public class Transaction
    {
        public DateTime Date { get; set; }
        public decimal Amount { get; set; }
        public string Category { get; set; }
        public TransactionType Type { get; set; }
    }
}
