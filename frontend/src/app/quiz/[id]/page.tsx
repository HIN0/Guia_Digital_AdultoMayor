type Props = {
  params: {
    id: string;
  };
};

export default function QuizPage({ params }: Props) {
  return <main>Quiz {params.id}</main>;
}
