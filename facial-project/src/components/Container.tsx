import './container.scss';

interface IProps {
  children: React.ReactNode;
}

const Container = ({ children }: IProps) => {
  return (
    <div className="wrapper">
      <div className="container">
        {children}
      </div>
    </div>
  );
}

export default Container;