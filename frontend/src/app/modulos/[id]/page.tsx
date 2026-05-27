type Props = {
  params: {
    id: string;
  };
};

export default function ModuloPage({ params }: Props) {
  return <main>Módulo {params.id}</main>;
}
