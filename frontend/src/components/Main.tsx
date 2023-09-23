import Register from "./Register";

function Main() {
  return (
    <div className="min-h-screen">
      {/* <header className=" bg-gradient-to-r from-black to-gray-900 text-white py-10">
         <h1 className="text-4xl font-bold text-center">
            Master English Speaking with Rachat: Your Path to Confident Communication
            Do you want to improve your spoken English effectively and
            with excitement? Rachat is here to help you!
        </h1>
      </header> */}
      <section className="max-w-5xl mx-auto p-6 ">
        <h1 className="text-4xl sm:text-6xl font-bold text-center mt-10 mb-5">
          Master English Speaking with Rachat: Your Path to Confident
          Communication
        </h1>
        <p className="text-xl sm:text-3xl leading-7 text-center">
          Your Personal English Speaking Coach. Speak fluently, gain confidence,
          and open doors to endless opportunities for personal and professional
          growth.
        </p>
        <p className="text-center my-5">
          <button
            className="bg-black hover:bg-gray-800 mx-auto text-white font-bold p-5 rounded-3xl mt-4 transition duration-300 ease-in-out"
            onClick={() => {
              // Azione da eseguire quando viene premuto il pulsante
            }}
          >
            START NOW
          </button>
        </p>
        <Register />

        <img src="../dist/assets/Img1_Rachat.png" alt="Image 1" className="rounded-3xl shadow-2xl my-8"/>
        <h2 className="mt-6 text-3xl font-semibold">What Does Rachat Do?</h2>
        <p className="text-lg leading-7">
          Rachat is a revolutionary English learning platform that allows you to
          have voice conversations with an AI-powered virtual assistant. Whether
          you're a student looking to perfect your pronunciation or a
          professional aiming to communicate confidently in English, Rachat is
          the perfect solution for you.
        </p>
        <img src="../dist/assets/Img2_Rachat.png" alt="Image 1" className="rounded-3xl shadow-2xl my-8"/>

        <h2 className="mt-6 text-2xl font-semibold">Our Key Features</h2>
        <ul className="list-square ml-6 mt-4 text-lg leading-7">
          <li>
            Guided Conversations: Practice English in real conversations with
            the help of our virtual assistant.
          </li>
          <li>
            Instant Feedback: Receive instant feedback on pronunciation and
            grammar to improve rapidly.
          </li>
          <li>
            Personalized Lessons: We tailor lessons to your needs and
            proficiency level.
          </li>
          <li>
            24/7 Access: Study whenever and wherever you want with our mobile
            app.
          </li>
          <li>
            Progress Tracking: Monitor your progress and see how your spoken
            English improves.
          </li>
        </ul>

        <h2 className="mt-6 text-2xl font-semibold">How It Works</h2>
        <ol className="list-decimal ml-6 mt-4 text-lg leading-7">
          <li>Sign Up: Register for free on Rachat and create your profile.</li>
          <li>
            Choose Your Lesson: Select a specific lesson or start with a free
            conversation.
          </li>
          <li>
            Start Speaking: Interact with our virtual assistant in English.
          </li>
          <li>
            Receive Feedback: Get instant feedback and tips for improvement.
          </li>
          <li>
            Track Your Progress: Monitor your achievements and keep track of
            your learning goals.
          </li>
        </ol>

        <p className="mt-6 text-lg leading-7">
          Ready to embark on your journey to enhance your spoken English?{" "}
          <a
            href="#"
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-300"
          >
            Sign up now
          </a>{" "}
          and discover how fun and effective learning English with us can be.
        </p>
      </section>
    </div>
  );
}

export default Main;
