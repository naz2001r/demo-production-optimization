# Demo Production optimization

## Runnig demo app :nut_and_bolt:
- Clone project;
- Run `streamlit run app.py` command in terminal.
## Description
**Demo app for product optimization in two ways:**
### 1. Maximization Profit:
  - **Table view:**
    |**resources**|**Product 1**|**Product 2**|**...**|**Product N**| Count|
    |---|---|---|---|---|--|
    |**resourse 1**|Resource costs 11|Resource costs 12|...|Resource costs 1N|*Resource count 1*|
    |**resourse 2**|Resource costs 21|Resource costs 22|...|Resource costs 2N|*Resource count 2*|
    |**...**|...|...|...|...|..|
    |**resourse M**|Resource costs M1|Resource costs M2|...|Resource costs MN|*Resource count M*|
    |**Profit**|*Profit 1*|*Profit 2*|...|*Profit N*|
  - **Mathematical form:**

    $$F(x) = \sum_{i=1}^n product_i*profit_i \to max$$

    $$\sum_{i=1}^n ResourceCost_ji*product_i <= ResourceCount_j \quad j=(1,m)$$

    $$product_i>=0 \quad i=(1,n)$$
      
### 2. Minimization Cost:
  - **Table view:**
    |**resources**|**Product 1**|**Product 2**|**...**|**Product N**| Count|
    |---|---|---|---|---|--|
    |**resourse 1**|Resource costs 11|Resource costs 12|...|Resource costs 1N|*Resource count 1*|
    |**resourse 2**|Resource costs 21|Resource costs 22|...|Resource costs 2N|*Resource count 2*|
    |**...**|...|...|...|...|..|
    |**resourse M**|Resource costs M1|Resource costs M2|...|Resource costs MN|*Resource count M*|
    |**Cost**|*Cost 1*|*Cost 2*|...|*Cost N*|
  - **Mathematical form:**

    $$F(x) = \sum_{i=1}^n product_i*profit_i \to min$$

    $$\sum_{i=1}^n ResourceCost_ji*product_i => ResourceCount_j \quad j=(1,m)$$

    $$product_i>=0 \quad i=(1,n)$$
      
      
    

      
      


