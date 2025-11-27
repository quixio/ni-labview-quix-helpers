These files are intended to help people post data to a Quix cloud hosted HTTP API. The `.vi` file is a basic starting point. Open it with LabVIEW then update the paths to the `main.py` file and the location of your Python executable.

**Note:** that at the time of writing, LabVIEW supports up to Python version `3.12`. Ensure that you have a valid Python version—other versions are unlikely to work.

# Tutorial: Sending Data from LabVIEW to Quix

This guide demonstrates how to stream data from a local LabVIEW environment into a Quix workspace using Python as a bridge. This setup allows you to utilize LabVIEW for data acquisition and control while leveraging Quix for real-time cloud processing and stream processing.

You can also follow the [tutorial video](https://youtu.be/cl1dPDqQNoI) which covers the same steps.

### **Prerequisites**

  * **LabVIEW**: Installed and capable of running Python Nodes (LabVIEW 2018 or later recommended).
  * **Python**: A compatible version installed locally (Python 3.12 is used in the tutorial video).
  * **Quix Account**: A workspace created in the [Quix Portal](https://portal.cloud.quix.io/).
    
-----

### **Part 1: Setting up the Quix Destination**

First, we need to create an ingestion point in Quix to receive the data.

1.  **Create an HTTP Source:**

      * Log in to your Quix Workspace.
      * Navigate to the **Connectors** page.
      * Search for and select the **HTTP API Source** connector.
      * This connector acts as a gateway to receive HTTP POST requests.

2.  **Configure the Topic:**

      * In the configuration settings, locate the **Output Topic** field.
      * Change the default name to something relevant, for example: `labview-data`.
        
3.  **Deploy:**

      * Click **Test connection & deploy**.
      * Wait for the service status to change to **Running**.
      * Once running, the service logs will appear in the bottom pane.
        
4.  **Get the URL:** Once running, copy the **Public URL** (e.g., `https://gateway-...quix.io`).
   
5.  **Verify (Optional):**

      * You can use a tool like Postman to send a test POST request to the generated URL to ensure data appears in the Quix "Messages" tab.

-----

### **Part 2: The LabVIEW Setup**
Open the `Post to Quix.vi`. This is the control center. The LabVIEW Virtual Instrument (VI) uses the native Python nodes to execute a script that handles the HTTP communication.

**The Block Diagram Architecture:**
The VI is structured using a standard `Open/Run/Close` Python session flow:

1.  **Open Python Session:**

      * This node initializes the Python environment.
      * **Input:** A constant string specifying the Python version (e.g., `3.12.7`).

2.  **Python Node (The Core):**

   This node executes the specific Python script. Here's how you define the parameters.
   
* **Input 1 (Path):** The file path to your local `main.py` script.
      
* **Input 2 (Module):** A constant string for the function name to call (e.g., `send_http_post`).
      
* **Input 3 (Parameters):** The data fields from your Front Panel controls are wired into this node as arguments. 
        For example: `TestID`, `SampleID`, `EnvironmentID`, `Operator Name`, etc.
        
* **Output:** An indicator wired to receive the return value (configured as a String for the JSON response).
    
3.  **Close Python Session:**

      * This node safely closes the Python instance after execution to free up resources.

-----

### **Part 3: The Local Python Bridge (`main.py`)**

LabVIEW calls a local Python script which handles the actual networking. This script acts as a "dumb" bridge. It doesn't decide *where* the data goes; it just listens to LabVIEW and executes the send command.

  * **Note:** Ensure your `main.py` file is in a known location (e.g., `C:\Users\You\Documents\Code\main.py`).

1.  **The Function:**

      * The script contains a function `send_http_post` that accepts arguments matching the LabVIEW inputs. Notice that it accepts `url` as an argument. This is key. We do **not** hardcode the URL here. We let LabVIEW tell Python where to send the data.

2.  **Payload Construction:**

      * Inside the function, the arguments are packed into a Python dictionary.

3.  **The Request:**

      * The script uses the `requests` library (`requests.post`) to send the dictionary as JSON data to the Quix URL.

**Important URL Configuration:**
You must configure the target URL in your Python script.

  * Copy the **Public URL** from your deployed Quix HTTP API Source.
  * **Crucial Step:** Paste the **Quix Public URL** you copied in Step 2.
  * Append `/data/` and a **Stream ID**.
  * **Final Format:** `https://[your-quix-gateway]/data/[your-stream-id]`
      * *Example:* `https://gateway-workspace.quix.io/data/demo-test-1`
      * *Why?* The "Stream ID" (the part after `/data/`) acts as the folder name in Quix. You can change this in LabVIEW (e.g., `demo-test-2`) to start a new data stream without restarting the code.

-----

### **Part 4: Customizing the Quix Response (Round-Trip)**

By default, the Quix HTTP Source might only return a generic status code (200 OK). To get useful feedback back into LabVIEW:

1.  **Edit the Quix Service:**

      * In the Quix portal, click **Edit Code** on your running HTTP API Source.
      * Open `main.py` within the online editor.

2.  **Modify the Return Statement:**

      * Locate the `post_data_with_key` function.
      * Instead of returning just a status code, create a dictionary containing relevant info (e.g., timestamps, status, or validation of received data).
      * Use `json.dumps` to format it.

    <!-- end list -->

    ```python
    # Example modification in Quix
    result = {
        "status": 200,
        "message": "Data received",
        "timestamp": str(datetime.now())
    }
    return json.dumps(result)
    ```

3.  **Sync and Redeploy:**

      * Click **Commit** and then **Sync to this commit** to redeploy the service with your changes.

-----

### **Part 5: Running the Integration**

1.  **Front Panel:** Open your LabVIEW Front Panel.
2.  **Input Data:** Fill in the text fields (Test ID, Sample ID, etc.).
3.  **Run:** Click the Run arrow on the VI.
4.  **Verify:**
      * **In LabVIEW:** The "JSON Response" indicator should populate with the custom message you defined in Part 4.
      * **In Quix:** Go to the **Messages** tab of your deployment. Select the `labview-data` topic. You will see your data rows appearing in real-time, tagged with the Stream ID you defined in the URL.

-----

### **Summary of Data Flow**

`LabVIEW Front Panel` -\> `Python Node` -\> `Local Python Script (Requests Lib)` -\> `Internet (HTTP POST)` -\> `Quix HTTP Source` -\> `Quix Topic`



