#The actual cypher given in the question
cypher="F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923CAB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84CC931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D963FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47EFD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63CED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A85A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794"
print("The actual cypher code is: \n{}\n".format(cypher))
hex_to_dec=[]
for i in range(0, len(cypher), 2):
    hex_to_dec.append(int(str('0x'+cypher[i:i+2]),0))                    #The second parameter for int is given as zero to include the padding if only 1 hex char is present
#print(hex_to_dec)
#print(len(hex_to_dec))

#Frequency of characters in english literature
freq={'A':0.08497,'B':0.01492,'C':0.02202,'D':0.04253,'E':0.11162,'F':0.02228,'G':0.02015,'H':0.06094,'I':0.07546,'J':0.00153,'K':0.01292,'L':0.04025,'M':0.02406,'N':0.06749,'O':0.07507,'P':0.01929,'Q':0.00095,'R':0.07587,'S':0.06327,'T':0.09356,'U':0.02758,'V':0.00978,'W':0.02560,'X':0.00150,'Y':0.01994,'Z':0.0077}
#print(freq)

def frequency_list_sum(list_of_elements):
    counts={}
    l=0
    for k in list_of_elements:
        l+=1
        counts[k]=counts.get(k,0)+1
    values=list(map(lambda x:x/l,list(counts.values())))
    sos=sum(map(lambda x: x ** 2,values))
    return sos

#To find the key lenth of the cypher
import numpy as np
max_dist=[]
for i in range(13):         #The key lengths we try are 1 to 13(as given in question)
    t=[hex_to_dec[j] for j in range(0,len(hex_to_dec),i+1)]
    max_dist.append(frequency_list_sum(t))
max_dist=np.array(max_dist)
key_length=np.argmax(max_dist)+1
print("We try the cypher with key lengths ranging from 1 to 13.\nAnd we find the value of summation of frequency square is greatest for the {} key length.\nTherefore the key length is {}\n".format(key_length,key_length))

def get_key(my_dict,val):
    for key, value in my_dict.items():
        if val == value:
            return key

def get_key_byte(n):
    t=t=[hex_to_dec[i] for i in range(0+n,len(hex_to_dec),key_length)]
    b={}
    for i in range(256):
        l=[ac^i for ac in t]
        if not any(char<32 or char>127 for char in l):
            l=list(map(lambda x:x.upper(),[chr(i) for i in l if 97<=i<=122]))       #Taking only the lowercase letters from each in situ deciphered codes and converting them to uppercase for matching the key of the freq table that contains the frequency of english charactes in the language
            q,summation={},0
            for k in l:
                q[k]=q.get(k,0)+1
                for kq,vq in q.items():
                    q[kq]=vq/26
                    for kp,vp in freq.items():
                        if kp==kq:
                            summation+=vp*vq
                b[i]=summation
    return get_key(b,max(list(b.values())))

key=[]
for i in range(key_length):
    key.append(get_key_byte(i))
print("The key is:")
print(key)
print()

message=[chr(hex_to_dec[i]^key[i%key_length]) for i in range(len(hex_to_dec))]
p=[]
w=[]
for i in message:
    if i==' ':
        p.append("".join(w))
        w=[]
    else:
        w.append(i)
p.append("".join(w))
print("The resultant message is:")
for i in range(len(p)):
    print(p[i],end=" ")
    if i%20==0 and i!=0:
        print()
