PROMPT_TEMPLATE = """
Your task is to design and implement a workflow that generates a network diagram featuring
virtual machines (VMs) based on customer specifications. The workflow should use a database
of VM types, detailing their descriptions, minimum specifications, and installed software 
that represents the network diagram, including VLANs and the specified
machines.

Question: {question} 

Context: {context} 

If you do not have any related information, please answer you don't know!

Answer:

"""