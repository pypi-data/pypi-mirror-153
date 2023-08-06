# Evolution of AI

timeline: https://aiartists.org/ai-timeline-art

1968: 2001 Space Odessey movie
1969: Shakey the robot SLAM by Minsky
1973: Harold Cohen at UCSD collaborated with AARON to create paintings
1987: Expert system "RI" at DEC to organized PC orders to save $40M/yr
1988: Watson used for machine translation
1990: Rodney Brooks starts pushing neural nets again
1995: ALICE chatbot based on text from WWW
1997: Deep Blue beat Garry Kasparov at Chess
2002: Rhoomba
2008: speech recognition on iPhone
2009: ImageNet by Fei-Fei Li (Stanford)
2011: Watson wins at Jeopardy
2012: unsupervised CV by Andrew Ng and Jeff Dean developed ability to recognize cat faces
2015: Google Deep Dream
2014: Chatbot "Eugene Goostman" passed the Turing Test
2018: AI art by [Obvious](http://obvious-art.com/) makes $432,500 at an auction


## Wikipedia

1997: Deep Blue beats Kasparov
~1998: web crawlers for information extraction
2002: Roomba
2004: DARPA grand challenge
2005: Honda's Asimo can walk as fast as a human and carry tray of food
2006: The Dartmouth Artificial Intelligence Conference
2007: Checkers is solved by researchers at U of Alberta
2009: Google's first autonomous car
2016: AlphaGo beats LeeSedol
2017: Asilomar Conference on Beneficial AI
2017: SAT problem solver solves (proves) the Pythagorean triples conjecture
2018: Google Duplex can book a table at a restaurant
2019: AlphaStar reaches Grandmaster level at StarCraft II, beating 99.8% of humans
2020: OpenAI's GPT-3


## Wikipedia Progress in AI

### Games

Draughts (checkers)     1994    21  31  Perfect     [7]
Othello (reversi)   1997    28  58  Perfect     [8]
Chess   1997    46  123     Perfect
Scrabble    2006                [9]
Shogi   2017    71  226     Perfect     [10]
Go  2016    172     360     Perfect
2p no-limit hold 'em    2017            Imperfect   [11]
StarCraft   -   270+        Imperfect   [12]
StarCraft II    2019

### Sub-human AI Capability

-   [Optical character recognition](https://en.wikipedia.org/wiki/Optical_character_recognition "Optical character recognition") for printed text (nearing par-human for Latin-script typewritten text)
-   [Object recognition](https://en.wikipedia.org/wiki/Object_recognition_(computer_vision) "Object recognition (computer vision)")\[_[clarification needed](https://en.wikipedia.org/wiki/Wikipedia:Please_clarify "Wikipedia:Please clarify")_\]
-   [Facial recognition](https://en.wikipedia.org/wiki/Facial_recognition_system "Facial recognition system"): Low to mid human accuracy (as of 2014)[\[47\]](https://en.wikipedia.org/wiki/Progress_in_artificial_intelligence#cite_note-47)
-   Visual question answering,[\[48\]](https://en.wikipedia.org/wiki/Progress_in_artificial_intelligence#cite_note-48) such as the VQA 1.0[\[49\]](https://en.wikipedia.org/wiki/Progress_in_artificial_intelligence#cite_note-49)
-   Various robotics tasks that may require advances in robot hardware as well as AI, including:
    -   Stable bipedal locomotion: Bipedal robots can walk, but are less stable than human walkers (as of 2017)[\[50\]](https://en.wikipedia.org/wiki/Progress_in_artificial_intelligence#cite_note-50)
    -   [Humanoid soccer](https://en.wikipedia.org/wiki/Robot_soccer "Robot soccer")[\[51\]](https://en.wikipedia.org/wiki/Progress_in_artificial_intelligence#cite_note-51)
-   [Speech recognition](https://en.wikipedia.org/wiki/Speech_recognition "Speech recognition"): "nearly equal to human performance" (2017)[\[52\]](https://en.wikipedia.org/wiki/Progress_in_artificial_intelligence#cite_note-52)
-   [Explainability](https://en.wikipedia.org/wiki/Explainable_artificial_intelligence "Explainable artificial intelligence"). Current medical systems can diagnose certain medical conditions well, but cannot explain to users why they made the diagnosis.[\[53\]](https://en.wikipedia.org/wiki/Progress_in_artificial_intelligence#cite_note-53)
-   [Stock market prediction](https://en.wikipedia.org/wiki/Stock_market_prediction "Stock market prediction"): Financial data collection and processing using Machine Learning algorithms
-   Various tasks that are difficult to solve without contextual knowledge, including:
    -   [Translation](https://en.wikipedia.org/wiki/Machine_translation "Machine translation")
    -   [Word-sense disambiguation](https://en.wikipedia.org/wiki/Word-sense_disambiguation "Word-sense disambiguation")
    -   [Natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing "Natural language processing")


### Deep Learning

2010: Word2vec, Mikolov, T.; et al. (2010). ["Recurrent neural network based language model"](http://www.fit.vutbr.cz/research/groups/speech/servite/2010/rnnlm_mikolov.pdf) (PDF). _Interspeech_: 1045–1048. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.21437/Interspeech.2010-343](https://doi.org/10.21437%2FInterspeech.2010-343). [Archived](https://web.archive.org/web/20170516181940/http://www.fit.vutbr.cz/research/groups/speech/servite/2010/rnnlm_mikolov.pdf) (PDF) from the original on 2017-05-16. Retrieved 2017-06-13.

### CNNs

2004: first GPU-accelerated CNNs
2010: MNIST solved with fully-connected networks on GPU
2011: CNNs for handwritten digits on GPU (MNIST)



### DL for NLP

material for chapter 5-7: https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing


Neural networks have been used for implementing language models since the early 2000s.[\[115\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-gers2001-115) LSTM helped to improve machine translation and language modeling.[\[116\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-NIPS2014-116)[\[117\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-vinyals2016-117)[\[118\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-gillick2015-118)

Other key techniques in this field are negative sampling[\[146\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-GoldbergLevy2014-146) and [word embedding](https://en.wikipedia.org/wiki/Word_embedding "Word embedding"). Word embedding, such as _[word2vec](https://en.wikipedia.org/wiki/Word2vec "Word2vec")_, can be thought of as a representational layer in a deep learning architecture that transforms an atomic word into a positional representation of the word relative to other words in the dataset; the position is represented as a point in a [vector space](https://en.wikipedia.org/wiki/Vector_space "Vector space"). Using word embedding as an RNN input layer allows the network to parse sentences and phrases using an effective compositional vector grammar. A compositional vector grammar can be thought of as [probabilistic context free grammar](https://en.wikipedia.org/wiki/Probabilistic_context_free_grammar "Probabilistic context free grammar") (PCFG) implemented by an RNN.[\[147\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-SocherManning2014-147) Recursive auto-encoders built atop word embeddings can assess sentence similarity and detect paraphrasing.[\[147\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-SocherManning2014-147) Deep neural architectures provide the best results for [constituency parsing](https://en.wikipedia.org/wiki/Statistical_parsing "Statistical parsing"),[\[148\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-148) [sentiment analysis](https://en.wikipedia.org/wiki/Sentiment_analysis "Sentiment analysis"),[\[149\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-149) information retrieval,[\[150\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-150)[\[151\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-151) spoken language understanding,[\[152\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-IEEE-TASL2015-152) machine translation,[\[116\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-NIPS2014-116)[\[153\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-auto-153) contextual entity linking,[\[153\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-auto-153) writing style recognition,[\[154\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-BROC2017-154) Text classification and others.[\[155\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-155)

Recent developments generalize [word embedding](https://en.wikipedia.org/wiki/Word_embedding "Word embedding") to [sentence embedding](https://en.wikipedia.org/wiki/Sentence_embedding "Sentence embedding").

[Google Translate](https://en.wikipedia.org/wiki/Google_Translate "Google Translate") (GT) uses a large end-to-end [long short-term memory](https://en.wikipedia.org/wiki/Long_short-term_memory "Long short-term memory") (LSTM) network.[\[156\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-GT_Turovsky_2016-156)[\[157\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-googleblog_GNMT_2016-157)[\[158\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-lstm1997-158)[\[159\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-lstm2000-159)[\[160\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-GoogleTranslate-160)[\[161\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-WiredGoogleTranslate-161) [Google Neural Machine Translation (GNMT)](https://en.wikipedia.org/wiki/Google_Neural_Machine_Translation "Google Neural Machine Translation") uses an [example-based machine translation](https://en.wikipedia.org/wiki/Example-based_machine_translation "Example-based machine translation") method in which the system "learns from millions of examples."[\[157\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-googleblog_GNMT_2016-157) It translates "whole sentences at a time, rather than pieces. Google Translate supports over one hundred languages.[\[157\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-googleblog_GNMT_2016-157) The network encodes the "semantics of the sentence rather than simply memorizing phrase-to-phrase translations".[\[157\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-googleblog_GNMT_2016-157)[\[162\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-Biotet-162) GT uses English as an intermediate between most language pairs.[\[162\]](https://en.wikipedia.org/wiki/Deep_learning#Natural_language_processing#cite_note-Biotet-162)