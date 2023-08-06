#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from gym.envs.registration import register

register(
    id='update2-v0',
    entry_point='gym_update2.envs:UpdateEnv2',
)

