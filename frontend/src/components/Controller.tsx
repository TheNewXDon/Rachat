import { useEffect, useState } from "react";
import Title from "./Title";
import RecordMessage from "./RecordMessage";
import axios from "axios";

function Controller() {
  //const user = JSON.parse(localStorage.getItem('user') ?? '');
  const userId = localStorage.getItem('user_id');
  const sessionId = 1;
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const [data, setData] = useState<any[]>([]);
  const [refresh, setRefresh] = useState(false);

  const handleRefresh = () => {
    setRefresh(!refresh);
  };
  const createBlobUrl = (data: any) => {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  };

  const getData = async () => {
    setIsLoading(true)
    try {
      
      const response = await axios.get(`http://localhost:8000/conversations?user_id=${userId}&session_id=${sessionId}`);
      setData(response.data)
      localStorage.setItem('last_messages', JSON.stringify(response.data));
      const messages = JSON.parse(localStorage.getItem('last_messages') ?? '');
      localStorage.setItem('last_user_id', messages[0].user_id);
      localStorage.setItem('last_session_id', messages[0].session_id);
      setIsLoading(false)
    } catch(err: any) {
      console.error(err.message);
      setIsLoading(false);
    };

    
  };

  useEffect(() => {
    getData();
  }, [])

  const listenSpeech = async (audio_file: string) => {
    try {
      const response = await axios.get(`http://localhost:8000/speech?audio_file=${audio_file}`, {responseType: 'blob'})
      const blob = new Blob([response.data], { type: 'audio/mpeg' });
      const audioUrl = URL.createObjectURL(blob);

      const audio = new Audio(audioUrl);
      audio.play()
    } catch (err: any) {
      console.error(err.message)
    }
  }

  /*const listenSpeechDB = async (audioUrl: string) => {
    try {
      const audio = new Audio(audioUrl);
      audio.play()
    } catch (err: any) {
      console.error(err.message)
    }
  }*/

  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);

    // Append recorded message to messages
    const myMessage = { sender: "me", blobUrl };
    const messageArr = [...messages, myMessage];

    // Convert blob url to blob object
    fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        // Construct audio to send file
        const formData = new FormData();
        formData.append("file", blob, "myFile.wav");

        // Send formData to API endpoint
        await axios
          .post(`http://localhost:8000/post-audio?user_id=${userId}&session_id=${sessionId}`, formData, {
            headers: { "Content-Type": "audio/mpeg" },
            responseType: "arraybuffer",
          })
          .then((res: any) => {
            getData()
            const blob = res.data;
            const audio = new Audio();
            audio.src = createBlobUrl(blob);

            // Append to audio
            const rachelMessage = { sender: "rachel", blobUrl: audio.src };
            messageArr.push(rachelMessage);
            setMessages(messageArr);

            
            // Play Audio
            setIsLoading(false);
            audio.play();
          })
          .catch((err) => {
            console.error(err.message);
            setIsLoading(false);
          });
      });
  };

  return (
    <div className="h-screen overflow-y-hidden bg-sky-100">
      <Title setMessages={setMessages} onRefresh={handleRefresh}></Title>
      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-64">
        <div className="mt-5 px-5 ">
          {/*messages.map((audio, index) => {
            return (
              <div
                key={index + audio.sender}
                className={
                  "flex flex-col " +
                  (audio.sender == "rachel" && "flex items-end")
                }
              >
                <div className="mt-4 ">
                  <p
                    className={
                      audio.sender == "rachel"
                        ? "ml-2 italic text-green-500"
                        : "mr-2 italic text-blue-500 text-right"
                    }
                  >
                    {audio.sender} 
                  </p>
                  <audio src={audio.blobUrl} className="appearance-none" controls />
                </div>
              </div>
            );
          })*/}
          <div className=" px-3 ">
            {data.map((mess, index) => {
              return (
                <div
                  key={index + mess.content}
                  className={
                    "flex flex-col " +
                    (mess.role == "assistant" && "flex")
                  }
                >
                  <div className=" ">
                    <p
                      className={
                        mess.role == "assistant"
                          ? "ml-4 italic text-blue-500"
                          : "mr-4 italic text-black text-right"
                      }
                    >
                      {mess.role == "assistant" ? "Rachel" : "Me"} 
                    </p>
                    <div className={"w-[48%] flex " + (mess.role == "user" ? "justify-end text-right ml-[52%] " : "")}>
                      <div onClick={mess.role != "user" ? () => listenSpeech(mess.audio) : () => console.log(mess.content)} className="bg-slate-200 border border-gray-400 rounded-3xl p-4 hover:cursor-pointer">
                        {mess.content}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
          { messages.length == 0 && data.length == 0 && !isLoading && (
            <div className="text-center font-light mt-10">Send Rachel a message...</div>
          )}

          { isLoading && (
            <div className="text-center font-light mt-10 animate-pulse">Give me a few seconds...</div>
          )}

        </div>
        <div className="fixed bottom-0 w-full py-1 border-t text-center bg-gradient-to-r from-slate-900 to-slate-700">
          <div className="flex justify-center items-center w-full ">
            <RecordMessage handleStop={handleStop}></RecordMessage>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Controller;
