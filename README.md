# Youtuber Analysis

**Youtuber Analysis** is a Python-based tool that provides detailed analytics for any YouTube channel. It generates a summary of the channel and provides recommendations of the top 5 videos among the latest 50 uploads. Additionally, the app offers basic information like the channel's display picture, name, ID, total subscribers, total videos, total views, and the location of the channel.
<table>
  <tr>
    <td>
      <img width="786" alt="ui" src="https://github.com/user-attachments/assets/99d29f69-057f-4490-a6ec-541eb0e034cf">
    </td>
    <td>
      <img width="803" alt="output" src="https://github.com/user-attachments/assets/078fb056-eaa5-407b-95fb-ab07d7aaac28">
    </td>
  </tr>
</table>

## Features

1. **Basic Channel Info**: 
   - Channel name, profile picture, ID, total subscribers, total views, total videos, and location.
   
2. **Channel Summary**: 
   - Generates a text-based summary of the YouTube channel using a language model.
   
3. **Top 5 Video Recommendations**: 
   - Recommends the top 5 rated videos (based on views) from the latest 50 videos uploaded by the channel.
   
4. **Link Validation**: 
   - Supports both types of YouTube channel links:
     - `https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxxxxxx`
     - `https://www.youtube.com/@xxxxxxxxxx`

## Files

### 1. `app.py`
   - **Description**: This file handles the Graphical User Interface (GUI) of the application. It takes the YouTube channel link as input and validates it. It has a button `Fetch Channel Info` to fetch the required data. The interface is divided into three sections:
     - **Section 1**: Displays basic information about the channel, including the profile picture.
     - **Section 2**: Provides a detailed summary of the channel.
     - **Section 3**: Recommends the top 5 videos from the channel based on views.
   - **Link Validation**: The application checks the format of the input link to ensure it follows one of the two accepted formats for YouTube channel URLs.

### 2. `youtuberData.py`
   - **Description**: This file interacts with the YouTube Data API to retrieve details about the channel. It gathers:
     - Channel name, logo (profile picture), total videos, subscribers, views, channel ID, and other key metrics.
     - It also fetches the top-rated videos from the latest 50 uploads.
   
### 3. `quantLlama.py`
   - **Description**: This file generates a summary of the YouTube channel using a large language model (LLM) called Llama. The summary is generated using a prompt and is limited to 200 tokens.
   - The LLM is powered by **TheBloke/Llama-2-7B-Chat-GGML**, which uses GGML quantization techniques to run efficiently on the CPU.

## Results

<table>
  <tr>
    <td>
      <img width="811" alt="typ12" src="https://github.com/user-attachments/assets/6b8936b7-4278-4264-9f36-816f1a30819c">
    </td>
    <td>
      <img width="803" alt="typ11" src="https://github.com/user-attachments/assets/0aeadcc0-0240-43f9-814a-fffd96b2d195">
    </td>
  </tr>
  <tr>
    <td>
      <img width="806" alt="typ21" src="https://github.com/user-attachments/assets/b9759c5d-8a94-4ef9-a47a-a1f064738429">
    </td>
    <td>
       <img width="797" alt="typ23" src="https://github.com/user-attachments/assets/e2cf74b4-1be9-494c-b680-8e998019cefe">
    </td>
  </tr>
</table>


## Learning from the Project

### Running Models on CPU with Quantization:
In this project, we explored the use of **quantization** to run large language models (LLMs) on a standard CPU. Quantization maps higher-precision values (like 32-bit floats) to lower-precision data types (such as 4-bit integers), significantly reducing memory and computational requirements without sacrificing too much accuracy. 

We used **CTransformers** from the `langchain_community.llms` library to download and run the model locally without needing external API calls. This approach enables developers to deploy sophisticated language models on everyday hardware.

### Quantization Techniques:
Several techniques were explored, such as GPTQ, ExLLama, NF4, bitsandbytes, and GGML. For this project, we used **GGML** quantization, which allowed us to efficiently run **Llama-2-7B** on local hardware.

### Challenges Faced:
- The first time you run the app, loading the summary of a YouTube channel may take **30-45 seconds** due to model initialization. However, with subsequent usage, text generation becomes faster as the model warms up.

## How to Run the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/dheerajkallakuri/youtuberAnalysis.git
   cd youtuberAnalysis
   ```

2. Install the required dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

Note: On first use, generating the summary might take some time due to the loading of the Llama model. Subsequent runs should be faster.
