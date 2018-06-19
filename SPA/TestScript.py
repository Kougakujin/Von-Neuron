## TEST SCRIPT

AGG = circonv(add(CORTEX['TRUE'], CORTEX['COUNT']), CORTEX['NO1'])
RET = add(circonv(AGG, inv(CORTEX['NO1'])), CORTEX['COUNT'])