import sys
from itertools import combinations
import csv
def readfile(file_name):
    try:
        transactions=[]
        with open(file_name,'r') as file:
            for line in file:
                line_list=line.strip().split()
                for i in range(len(line_list)):
                    line_list[i]=int(line_list[i])
                sorted(line_list)
                transactions.append(line_list)
            return transactions
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except Exception as e:
        print(f"A error occurred: {e}")

    
def find_L1(transactions,min_sup):
    C1={}
    for transaction in transactions:
        for item in transaction:
            if item not in C1:
                C1[item]=1
            else:
                C1[item]+=1
    print(len(C1))

    L1={}
    for item in C1:
        if C1[item]>=min_sup:
            key=frozenset([item])
            L1[key]=C1[item]
            #L1[frozenset(item)]=C1[item]
    print(len(L1))
    return L1




def find_Lk(C,transactions,min_sup):
    for itemset in C:
        for transaction in transactions:
            if itemset.__le__(transaction):
                C[itemset]+=1
    L={}
    for itemset in C:
        if C[itemset]>=min_sup:
            L[itemset]=C[itemset]
    return L

def output_format_processing(output_list):
	for i in range(len(output_list)):
		LHS_string=""
		LHS_string+="{"
		for j in output_list[i][0]:
			LHS_string+=f"{j} " 
		LHS_string=LHS_string[:-1]
		LHS_string+="}"
		output_list[i][0]=LHS_string

		RHS_string=""
		RHS_string+="{"
		for j in output_list[i][1]:
			RHS_string+=f"{j} " 
		RHS_string=RHS_string[:-1]
		RHS_string+="}"
		output_list[i][1]=RHS_string



def main():
    if len(sys.argv) != 4:
        print("Usage: python association_rule.py min_sup min_conf file_name")
        return

    min_sup = int(sys.argv[1])
    min_conf = float(sys.argv[2])
    file_name = sys.argv[3]

    print("min_sup:", min_sup)
    print("min_conf:", min_conf)
    print("file_name:", file_name)
    transactions=readfile(file_name)
    n=len(transactions)
    print(len(transactions))
    L1=find_L1(transactions,min_sup)
    for i in range(len(transactions)):
        transactions[i]=frozenset(transactions[i])
    frequency_itemset={}
    for itemset in L1:
        frequency_itemset[itemset]=L1[itemset]
    original_frequency_itemset_len=0
    K=1
    C={}
    L={}
    L=L1
    L2={}
    while(len(frequency_itemset)-original_frequency_itemset_len>0):
        print(f"Find L{K+1}")
        original_frequency_itemset_len=len(frequency_itemset)
        C={}
        for itemset_1 in L:
            for itemset_2 in L:
                if len(itemset_1^itemset_2)==2:
                    if K==1:
                        if itemset_1|itemset_2 not in C:
                            C[itemset_1|itemset_2]=0
                    else:
                        if(itemset_1^itemset_2 not in L2):
                            continue
                        else:
                            if itemset_1|itemset_2 not in C:
                                C[itemset_1|itemset_2]=0
        L=find_Lk(C,transactions,min_sup)
        if K==1:
            L2=L
        for itemset in L:
            if itemset not in frequency_itemset:
                frequency_itemset[itemset]=L[itemset]
        K+=1
    print(f"frequency itemset=\n{frequency_itemset}")
    print(f"frequency_itemset_length={len(frequency_itemset)}")
    StrongAssociationRules=[]
    output=[]
    for FIS in frequency_itemset:
        if len(FIS)>1:
            for j in range(1,len(FIS)):
                for LHS in list(combinations(FIS,j)):
                    RHS=FIS-frozenset(LHS)
                    now_conf=frequency_itemset[FIS]/frequency_itemset[frozenset(LHS)]
                    if now_conf>=min_conf:
                        StrongAssociationRules.append([LHS,tuple(RHS),format(frequency_itemset[FIS]),format(now_conf,".3f")])
                        output.append([LHS,RHS,format(frequency_itemset[FIS]),format(now_conf,".3f")])
    output_format_processing(output)
    # print("rule length=",len(output))
    # for SAR in StrongAssociationRules:
    #     print(f"{SAR[0]}->{SAR[1]},sup={SAR[2]},conf={SAR[3]}")
    print(f"num of StrongAssociationRule={len(StrongAssociationRules)}")
    #print(output)
    # Write output to file
    with open('output.csv', 'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["LHS","RHS", "support", "confidence"])
        writer.writerows(output)

    


if __name__ == "__main__":
    main()