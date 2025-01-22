from compare import Spearman_s_Footrule


if __name__ == "__main__":
    rank1 = [4,2,1,3]
    rank2 = [2,4,3,1]
    rank3 = [4,2,3,1]
    rank4 = [3,1,2,4]
    print(Spearman_s_Footrule(rank1,rank2))
    print(Spearman_s_Footrule(rank1,rank3))
    print(Spearman_s_Footrule(rank1,rank4))


    
