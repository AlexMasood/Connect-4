# Connect-4
Simple command line connect 4 game featuring an ai taught through reinforcement learning.

Training an ai on the 6 by 7 standard connnect 4 grid takes too long to make any meaningful training.\
A potential solution to this is to train on a 4 by 4 grid and apply this 12 times on the grid for each possible time a 4 by 4 grid can appear on a 6 by 7 grid.

It should be noted that the majority of games will result in the ai picking unexplored routes, this means that the bored is unfamiliar to the ai and will lead to it choosing the last legal move. This is due to the large amount of combinations of board states that can be made (4531985219092 combinations) this number is far too large to train, using this training method.\
Anoher consideration is that the dictionary size grows incredibly large, 250MB per ai for 1000000 games trained.\
Below is a link to policies that has been trained for 1000000 games.\
https://drive.google.com/drive/folders/1P0VLg3rJffNroS11PcBI39mPWYDp_Ibi?usp=sharing
