import React from "react";

const Tree = ({ data }) => {
  if (!data || !data.tree) {
    return <div>Нет данных</div>;
  }
    console.log(data)
  const renderParentChain = () => {
    if (!data.tree.parent || data.tree.parent.length === 0) {
      return null;
    }

    return (
      <div style={{ marginBottom: "20px" }}>
        <div style={{ fontWeight: "bold", marginBottom: "5px" }}>
          Родительская цепочка:
        </div>
        {data.tree.parent.map((parent, index) => (
          <div
            key={parent.id}
            style={{
              marginLeft: `${index * 20}px`,
              display: "flex",
              alignItems: "center"
            }}
          >
             {parent.name}
          </div>
        ))}
      </div>
    );
  };

  const renderChildren = () => {
    if (!data.tree.children || data.tree.children.length === 0) {
      return (
        <div style={{ fontStyle: "italic", color: "#999" }}>
          Нет дочерних элементов
        </div>
      );
    }

    return (
      <div>
        <div style={{ fontWeight: "bold", marginBottom: "5px" }}>
          Дочерние элементы:
        </div>
        {data.tree.children.map((child) => (
          <div
            key={child.id}
            style={{
              marginLeft:child.type === "Location" ? "20px" : "30px",
              display: "flex",
              alignItems: "center",
              marginBottom: "5px"
            }}
          >
            {child.name}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div style={{
      fontFamily: "monospace",
      lineHeight: "1.8em",
      padding: "15px",
      border: "1px solid #eee",
      borderRadius: "5px"
    }}>
      <div style={{
        fontWeight: "bold",
        fontSize: "1.2em",
        marginBottom: "15px",
        display: "flex",
        alignItems: "center"
      }}>
        <span style={{ marginLeft: "10px" }}>
          ({data.object.type})
        </span>
      </div>

      {renderParentChain()}
      {renderChildren()}
    </div>
  );
};

export default Tree;