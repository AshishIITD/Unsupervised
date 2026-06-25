import numpy as np
import matplotlib.pyplot as plt
import os
from itertools import combinations

class CustomApriori:
    """
    A clean, from-scratch implementation of the Apriori algorithm for finding
    frequent itemsets and mining association rules, designed for educational clarity.
    """
    def __init__(self, min_support=0.2, min_confidence=0.5):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = {} # Maps itemset tuple to its support
        self.rules = []             # List of dicts containing rules details

    def fit(self, transactions):
        self.transactions = [set(t) for t in transactions]
        self.n_transactions = len(transactions)
        
        # Extract unique items
        unique_items = set()
        for t in self.transactions:
            unique_items.update(t)
        self.items = sorted(list(unique_items))
        
        # 1. Generate Frequent 1-itemsets
        # Format: itemset is represented as a sorted tuple
        c1 = [ (item,) for item in self.items ]
        l1 = self._filter_candidates(c1)
        
        current_l = l1
        k = 2
        while len(current_l) > 0:
            # 2. Generate Candidate k-itemsets (Join Step)
            candidates = self._generate_candidates_k(list(current_l.keys()), k)
            
            # 3. Filter Candidate k-itemsets by Support (Scan Step)
            lk = self._filter_candidates(candidates)
            
            if len(lk) == 0:
                break
                
            # Add to main frequent itemset registry
            self.frequent_itemsets.update(lk)
            current_l = lk
            k += 1
            
        # 4. Generate Association Rules
        self._generate_rules()
        return self

    def _filter_candidates(self, candidates):
        """
        Scans the transactions to count support for each candidate itemset
        and filters out those below the min_support threshold.
        """
        counts = {}
        for candidate in candidates:
            cand_set = set(candidate)
            for t in self.transactions:
                if cand_set.issubset(t):
                    counts[candidate] = counts.get(candidate, 0) + 1
                    
        # Filter by minimum support
        frequent = {}
        for candidate, count in counts.items():
            support = count / self.n_transactions
            if support >= self.min_support:
                frequent[candidate] = support
                
        return frequent

    def _generate_candidates_k(self, prev_frequent, k):
        """
        Joins frequent (k-1)-itemsets to create candidate k-itemsets.
        Includes pruning step: a candidate is pruned if any of its (k-1) subsets
        are not frequent.
        """
        candidates = []
        n_prev = len(prev_frequent)
        
        for i in range(n_prev):
            for j in range(i + 1, n_prev):
                # Join condition: if the first k-2 elements are identical
                itemset1 = prev_frequent[i]
                itemset2 = prev_frequent[j]
                
                if itemset1[:-1] == itemset2[:-1]:
                    candidate = tuple(sorted(list(set(itemset1 + itemset2))))
                    
                    # Pruning: check if all (k-1) subsets of candidate are frequent
                    if self._all_subsets_frequent(candidate, prev_frequent, k - 1):
                        candidates.append(candidate)
                        
        return candidates

    def _all_subsets_frequent(self, candidate, prev_frequent, k_minus_1):
        """
        Checks if all subsets of size (k-1) of the candidate itemset are present
        in the previous frequent itemsets list.
        """
        subsets = list(combinations(candidate, k_minus_1))
        prev_frequent_set = set(prev_frequent)
        
        for s in subsets:
            if tuple(sorted(s)) not in prev_frequent_set:
                return False
        return True

    def _generate_rules(self):
        """
        Generates association rules from frequent itemsets of size >= 2.
        Calculates Support, Confidence, and Lift.
        """
        self.rules = []
        
        # We only look at frequent itemsets of size >= 2
        for itemset, support_I in self.frequent_itemsets.items():
            if len(itemset) < 2:
                continue
                
            # Find all non-empty proper subsets of the itemset
            itemset_set = set(itemset)
            for size in range(1, len(itemset)):
                subsets = [set(s) for s in combinations(itemset, size)]
                
                for antecedent in subsets:
                    consequent = itemset_set - antecedent
                    
                    antecedent_tuple = tuple(sorted(list(antecedent)))
                    consequent_tuple = tuple(sorted(list(consequent)))
                    
                    # Support of antecedent
                    # Note: We need to look up support. If it's a 1-itemset, it might not be in
                    # frequent_itemsets registry if we skipped saving 1-itemsets (we saved them in l1 though).
                    # Actually, we should make sure we have support of antecedent. Let's calculate on the fly or look up.
                    support_A = self._get_support_of(antecedent_tuple)
                    support_C = self._get_support_of(consequent_tuple)
                    
                    if support_A == 0 or support_C == 0:
                        continue
                        
                    # Confidence = Support(A U C) / Support(A)
                    confidence = support_I / support_A
                    
                    if confidence >= self.min_confidence:
                        # Lift = Confidence(A -> C) / Support(C)
                        lift = confidence / support_C
                        
                        self.rules.append({
                            'antecedent': antecedent_tuple,
                            'consequent': consequent_tuple,
                            'support': support_I,
                            'confidence': confidence,
                            'lift': lift
                        })

    def _get_support_of(self, itemset_tuple):
        """
        Helper to get support of any itemset (frequent or not) on the fly.
        """
        # If already registered, return it
        if itemset_tuple in self.frequent_itemsets:
            return self.frequent_itemsets[itemset_tuple]
            
        # Otherwise count from transactions
        count = 0
        cand_set = set(itemset_tuple)
        for t in self.transactions:
            if cand_set.issubset(t):
                count += 1
        return count / self.n_transactions

def generate_grocery_transactions():
    """
    Generates a synthetic list of grocery store transactions.
    Items: Bread, Butter, Milk, Eggs, Diapers, Beer, Coke, Chips
    Contains hidden patterns:
    - {Bread} -> {Butter} (Very high support and confidence)
    - {Beer} -> {Chips, Coke} (High lift - party purchases)
    - {Diapers} -> {Beer} (Classic retail association rule)
    """
    transactions = [
        ['Bread', 'Butter', 'Milk', 'Eggs'],
        ['Bread', 'Butter', 'Milk'],
        ['Bread', 'Butter', 'Coke'],
        ['Beer', 'Chips', 'Coke'],
        ['Diapers', 'Beer', 'Chips'],
        ['Diapers', 'Beer', 'Milk', 'Bread'],
        ['Diapers', 'Beer', 'Butter'],
        ['Bread', 'Butter', 'Milk', 'Eggs', 'Coke'],
        ['Beer', 'Chips'],
        ['Milk', 'Eggs'],
        ['Bread', 'Butter'],
        ['Diapers', 'Beer', 'Chips', 'Coke'],
        ['Bread', 'Butter', 'Eggs'],
        ['Beer', 'Chips', 'Coke'],
        ['Diapers', 'Beer', 'Chips', 'Bread', 'Butter']
    ]
    return transactions

def main():
    print("=" * 70)
    print("   UNSUPERVISED LEARNING: APRIORI ASSOCIATION RULE MINING DEMO")
    print("=" * 70)
    
    # 1. Generate data
    transactions = generate_grocery_transactions()
    print(f"[*] Generated grocery database: {len(transactions)} transaction baskets.")
    print("    Baskets contain combinations of: Bread, Butter, Milk, Eggs, Diapers, Beer, Chips, Coke")
    print("    We want to find which items are purchased together and quantify their relationship.")
    
    # 2. Fit Custom Apriori
    # min_support = 25% (must appear in at least 4 out of 15 transactions)
    # min_confidence = 60% (rule must be true at least 60% of the time)
    min_support = 0.25
    min_confidence = 0.60
    apriori = CustomApriori(min_support=min_support, min_confidence=min_confidence)
    apriori.fit(transactions)
    
    # 3. Analyze rules
    rules = apriori.rules
    print("\n" + "-" * 50)
    print("📊 ALGORITHM RESULTS (TECHNICAL & LAYMAN TRANSATION)")
    print("-" * 50)
    print(f"Parameters: Min Support = {min_support*100:.0f}%, Min Confidence = {min_confidence*100:.0f}%")
    print(f"Frequent Itemsets Found: {len(apriori.frequent_itemsets)}")
    print(f"Association Rules Discovered: {len(rules)}")
    
    print("\n📢 Layman Narrative Interpretation:")
    print("-> How Association Rules work:")
    print("   We measure relationships using three core dials:")
    print("   1. Support (Popularity): How often the items are bought together. (e.g., '1 in 4 transactions')")
    print("   2. Confidence (Reliability): The 'if-then' probability. 'If they buy A, how often do they also buy B?'")
    print("   3. Lift (Strength): How much buying A boosts buying B compared to random chance.")
    print("      - Lift = 1: A and B are independent. No relationship.")
    print("      - Lift > 1: Strong bond! (e.g., Lift of 3 means they are 3 times more likely to buy B together)")
    
    print("\n🔍 Strongest Discovered Rules:")
    # Sort rules by Lift descending
    sorted_rules = sorted(rules, key=lambda x: x['lift'], reverse=True)
    for idx, r in enumerate(sorted_rules[:5]):
        ant = ", ".join(r['antecedent'])
        cons = ", ".join(r['consequent'])
        support = r['support'] * 100
        confidence = r['confidence'] * 100
        lift = r['lift']
        
        # Dynamic layman business commentary
        if lift > 2.0:
            comm = "💡 Golden Rule! Perfect for product bundling or co-locating on the shelf."
        elif confidence > 80.0:
            comm = "🛡️ High Reliability. You can safely recommend the second item at checkout."
        else:
            comm = "📈 Good correlation. Worth monitoring or running a coupon promotion."
            
        print(f"\nRule {idx+1}: If a customer buys [{ant}] -> then they buy [{cons}]")
        print(f"   - Support (Popularity): {support:.1f}% of all transactions")
        print(f"   - Confidence (Reliability): {confidence:.1f}% of the time")
        print(f"   - Lift (Strength Multiplier): {lift:.2f}x increase")
        print(f"   - Business Interpretation: {comm}")

    # 4. Plot and save (Scatter/Bubble Plot of Rules)
    if len(rules) > 0:
        os.makedirs("/home/gaian/Unsupervised/python/association", exist_ok=True)
        plt.figure(figsize=(10, 6), facecolor='#121214')
        ax = plt.axes()
        ax.set_facecolor('#1e1e24')
        
        supports = [r['support'] for r in rules]
        confidences = [r['confidence'] for r in rules]
        lifts = [r['lift'] for r in rules]
        
        # Bubble sizes proportional to lift
        sizes = [l * 100 for l in lifts]
        
        # Color based on lift
        scatter = plt.scatter(supports, confidences, s=sizes, c=lifts, cmap='plasma', 
                              alpha=0.85, edgecolors='#ffffff', linewidths=0.5)
        
        cbar = plt.colorbar(scatter, shrink=0.8)
        cbar.ax.yaxis.set_tick_params(color='#cccccc')
        cbar.ax.yaxis.label.set_color('#cccccc')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#cccccc')
        cbar.set_label('Rule Lift (Strength)', fontsize=11, color='#cccccc', labelpad=10)
        
        # Annotate a couple of rules
        for i, r in enumerate(rules):
            if r['lift'] > 1.8 or r['confidence'] > 0.85:
                ant_str = "+".join(r['antecedent'])
                cons_str = "+".join(r['consequent'])
                plt.annotate(f"{ant_str}→{cons_str}", 
                             xy=(r['support'], r['confidence']),
                             xytext=(r['support'] + 0.005, r['confidence'] + 0.01),
                             color='#ffffff', fontsize=8, alpha=0.9,
                             bbox=dict(boxstyle="round,pad=0.2", fc="#2a2a35", ec="#555566", lw=0.5))
        
        plt.title('Association Rules Explorer (Apriori)', fontsize=14, color='#ffffff', pad=15)
        plt.xlabel('Support (Rule Popularity)', fontsize=11, color='#cccccc')
        plt.ylabel('Confidence (Rule Reliability)', fontsize=11, color='#cccccc')
        
        # Format axes
        ax.tick_params(colors='#cccccc')
        ax.spines['bottom'].set_color('#333333')
        ax.spines['left'].set_color('#333333')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.grid(color='#333333', linestyle='--', alpha=0.3)
        
        # Pad axes for annotations
        plt.xlim(min(supports) - 0.05, max(supports) + 0.1)
        plt.ylim(min(confidences) - 0.05, max(confidences) + 0.05)
        
        output_path = "/home/gaian/Unsupervised/python/association/apriori_result.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"\n[+] Visualization successfully saved to: {output_path}")
    else:
        print("\n[!] No rules found with current thresholds, skipping plot.")
        
    print("=" * 70)

if __name__ == '__main__':
    main()
