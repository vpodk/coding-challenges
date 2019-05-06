// The data given
const mockResponse = {
  "questions": [{
    "id": 1,
    "text": "Favorite color",
    "answers": [{
      "id": 1,
      "text": "Red",
      "responses": 10
    }, {
      "id": 2,
      "text": "Green",
      "responses": 20
    }, {
      "id": 3,
      "text": "Blue",
      "responses": 5
    }]
  }, {
    "id": 2,
    "text": "Favorite animal",
    "answers": [{
        "id": 1,
        "text": "Dog",
        "responses": 150
      }, {
        "id": 2,
        "text": "Cat",
        "responses": 100
      }, {
        "id": 3,
        "text": "Bird",
        "responses": 17
      }]
    }
  ]
}


class Poll extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedQuestion: props.questions[Math.floor(Math.random() * props.questions.length)],
      selectedAnswer: null
    };
  }

  selectAnswer(selectedAnswer) {
    this.setState({ selectedAnswer });

    if (this.props.addVote) {
      this.props.addVote(this.state.selectedQuestion.id, selectedAnswer.id);
    }
  }

  render() {
    let selectedAnswerResponses;

    if (this.state.selectedAnswer) {
      let selectedQuestion = this.props.questions
        .filter(question => question.id === this.state.selectedQuestion.id)[0];

      selectedAnswerResponses = selectedQuestion.answers
        .filter(answer => answer.id === this.state.selectedAnswer.id)[0].responses;
    }

    return this.state.selectedAnswer ? (
      <div>
        You selected: {this.state.selectedAnswer.text} {' '}
        ({selectedAnswerResponses} responses)
        <div>
          <h4>Other potential answers</h4>
          <ul>
          {this.state.selectedQuestion.answers
            .filter(answer => answer !== this.state.selectedAnswer)
            .map(answer => (
              <li key={answer.id}>{answer.text} - {answer.responses} responses</li>
          ))}
          </ul>
        </div>
      </div>
    ) : (
      <Question
        data={this.state.selectedQuestion}
        onAnswerSelected={answer => this.selectAnswer(answer)} />
    );
  }
}

class Question extends React.Component {
  render() {
    let question = this.props.data;

    return (
      <div>
        <form onSubmit={() => this.props.onAnswerSelected(this.state.answer)}>
          <fieldset>
            <legend>What is your {question.text.toLowerCase()}?</legend>
            {question.answers.map(answer => (
              <div key={answer.id}>
                <label>
                  <input type="radio" name="answer" value={answer.text}
                         onClick={() => this.setState({answer: answer})} />
                  {' '}
                  {answer.text}
                </label>
              </div>
            ))}
            <button type="submit">Submit</button>
          </fieldset>
        </form>
      </div>
    );
  }
}

const ADD_VOTE = 'ADD_VOTE';
const voteActionCreator = (questionId, answerId) => ({
  type: ADD_VOTE,
  payload: {
    questionId,
    answerId
  }
});

function questionReducer(state, action) {
  state = state || [];

  switch (action.type) {
    case ADD_VOTE:
      let { questionId, answerId } = action.payload;
      let newState = state.map(question => Object.assign({}, question, {
        answers: (question.answers || [])
          .map(answer => Object.assign({}, answer, {
            responses: answer.responses + (answer.id === answerId && question.id === questionId ? 1 : 0)
          }))
      }));

      return newState;
    default:
      return state;
  }
}

const store = Redux.createStore(questionReducer, mockResponse.questions);
const mapDispatchToProps = dispatch =>
  Redux.bindActionCreators({ addVote: voteActionCreator }, dispatch);
const mapStateToProps = (state) => ({ questions: state });
const PollContainer = ReactRedux.connect(mapStateToProps, mapDispatchToProps)(Poll);
const Provider = ReactRedux.Provider;

ReactDOM.render(
  <Provider store={store}>
    <PollContainer />
  </Provider>,
  document.getElementById('root')
);
