# DoctorMoon
An analysis system for scientific publications using the principle of self-citation. 
Currently based on the S2 corpus: https://labs.semanticscholar.org/corpus/

## TLDR
Scientific papers can be classified into concept cycles by starting from a single paper, exploring all of its incoming and outgoing references, 
then processing those papers' in-out references for some N depth, and then pruning out any papers the original authors didn't use in their own later 
papers. 
This creates a connected cycle of important papers related to the starting paper, as shown by in the original authors' citation behavior.
