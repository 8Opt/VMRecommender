from vmrec.faiss import FAISS
from vmrec.agent import TinyAgent
from vmrec.utils import yaml_load


config = yaml_load(dir='./config.yaml')

network_diagram_request_samples = {
    "Security": "I want a network diagram that clearly illustrates our security posture. I need to see how our firewalls are configured and where they sit within the network, along with any other security devices like intrusion detection systems (IDS). I'd like to see the flow of traffic between our internal network and the internet, showing any DMZs or other segmentation measures. The diagram should also highlight any potential vulnerabilities, like open ports or exposed services, so we can prioritize remediation efforts.",

    "Scalability and Performance": "I want a network diagram that showcases how our network is designed to scale and handle increasing traffic. It should depict how our load balancers are set up and how they distribute traffic across multiple servers. I'd like to see the bandwidth of each connection and the capacity of our core network devices to understand any potential bottlenecks. The diagram should also clearly show how our network is segmented to optimize performance for specific applications, like our web server or database cluster.",

    "Cloud Integration": "I want a network diagram that illustrates how our on-premises infrastructure connects to our cloud services. It should show how our servers communicate with our cloud-based applications and databases, including any VPNs or dedicated connections. The diagram should also highlight any security measures we have in place for cloud access, like multi-factor authentication or cloud-based firewalls. Finally, I want to understand how our cloud provider's network architecture integrates with our own network.",

    "Collaboration and Communication": "I want a network diagram that maps out how our employees and teams collaborate and communicate using various technologies. It should show how our internal network connects to our voice over IP (VoIP) system, video conferencing platforms, and collaboration tools like Microsoft Teams or Slack. The diagram should also highlight any dedicated network segments for these applications to ensure optimal performance and minimize latency.",

    "Disaster Recovery and Business Continuity": "I want a network diagram that visualizes our disaster recovery plan and business continuity measures. It should show how our network is designed to handle outages and ensure critical services remain available. This includes identifying backup servers, redundant connections, and any failover mechanisms in place. The diagram should also clearly show how our data is replicated and backed up, both within our network and in the cloud, to ensure data integrity and business continuity.",
}


faiss_storing = FAISS(config=config['faiss_settings'], 
                      data_dir='./vm_info.csv')

llm = TinyAgent(config=config['chat_model'])


if __name__ == "__main__": 
    user_query = network_diagram_request_samples["Cloud Integration"]
    context = faiss_storing.query(input=user_query)

    # context's type is pd.DataFrame, convert it into str
    addtional_info = ""
    for _, row in context.iterrows():
        addtional_info += row.text + "\n"

    result = llm.query(input=user_query, 
                       context=context)    
    
    # Extract information from the result
    result = result.split("<|assistant|>")[-1]
    print(result)

"""
To generate a network diagram using virtual machines (VMs) with their corresponding network settings, we would:

1. Collect all the virtual machines of interest from our cloud provider. 

2. Create a database for storing VM types, descriptions, minimum specifications, and installed software.

3. Develop a Python script to extract the network information from each VM using the available APIs.

4. Use Python libraries like NetworkX to represent the network diagram using VLANs and network configurations.

5. Create high-quality network diagrams using the network representation we have built.


In this diagram, we have a standard network topography with the virtual machines in different VLANs, and VLAN 25, which represents the internal WAN network, is connected to VLAN 13 for internal traffic. The routers associated with each VLAN and the physical network interface cards of each VM are also included for easier visualization. The firewall in our solution is represented in the diagram by VLAN 5000.

Hope this helps! Let me know if you have any other questions.
"""