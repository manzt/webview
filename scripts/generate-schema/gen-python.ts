import { type Doc, isComplexType, type Node } from "./parser.ts";
import { match, P } from "npm:ts-pattern";
import { Writer } from "./gen-helpers.ts";
import { assert } from "jsr:@std/assert";

const header = (relativePath: string) =>
  `# DO NOT EDIT: This file is auto-generated by ${relativePath}\n` +
  "from enum import Enum\n" +
  "from typing import Any, Literal, Optional, Union\n" +
  "import msgspec\n\n";

export function generatePython(
  doc: Doc,
  name: string,
  relativePath: string,
): string {
  return header(relativePath) + generateTypes(doc, name);
}

function generateTypes(
  doc: Doc,
  name: string,
) {
  const writer = new Writer();

  let definitions = "";
  const skipAssignments = ["object", "intersection", "enum", "union"];
  for (const [name, definition] of Object.entries(doc.definitions)) {
    const definitionWriter = new Writer();
    const { w, wn } = definitionWriter.shorthand();
    if (!skipAssignments.includes(definition.type)) {
      w(name, " = ");
    }
    generateNode(definition, definitionWriter);
    if (definition.description) {
      wn('"""');
      wn(`${definition.description}`);
      wn('"""');
    }
    definitions += definitionWriter.output();
  }

  const { w, wn } = writer.shorthand();

  if (!skipAssignments.includes(doc.root.type)) {
    w(name, " = ");
  }
  generateNode(doc.root, writer);
  if (doc.description && doc.root.type !== "object") {
    wn('"""');
    wn(`${doc.description}`);
    wn('"""');
  }

  return definitions + writer.output();
}

function sortByRequired<T extends { required: boolean }>(
  properties: T[],
): T[] {
  return [...properties].sort((a, b) => {
    if (a.required === b.required) return 0;
    return a.required ? -1 : 1;
  });
}

function generateNode(node: Node, writer: Writer) {
  const { w, wn } = writer.shorthand();
  using context = new Context(node);
  match(node)
    .with({ type: "reference" }, ({ name }) => w(name))
    .with({ type: "int" }, () => w("int"))
    .with({ type: "float" }, () => w("float"))
    .with({ type: "boolean" }, () => w("bool"))
    .with({ type: "string" }, () => w("str"))
    .with({ type: "literal" }, (node) => w(`Literal["${node.value}"]`))
    .with(
      { type: "record" },
      (node) => w(`dict[str, ${mapPythonType(node.valueType)}]`),
    )
    .with({ type: "enum" }, (node) => {
      wn(`class ${node.name}(str, Enum):`);
      for (const value of node.members) {
        wn(`    ${value} = "${value}"`);
      }
      wn("");
    })
    .with({ type: "union" }, (node) => {
      const depWriter = new Writer();
      const classes = node.members.map((m) => {
        if (isComplexType(m)) {
          generateNode(m, depWriter);
        }
        if (m.name) return m.name;
        const ident = m.type === "object"
          ? m.properties?.find((p) => p.required)?.key ?? ""
          : "";
        return `${node.name}${cap(ident)}`;
      });
      writer.append(depWriter.output());
      wn(`${node.name} = Union[${classes.join(", ")}]`);
    })
    .with({ type: "object" }, (node) => {
      match(context.parent)
        .with({ type: "union" }, (parent) => {
          const name = context.closestName();
          const ident = node.properties.find((p) => p.required)?.key ?? "";
          wn(
            `class ${name}${
              cap(ident)
            }(msgspec.Struct, kw_only=True, omit_defaults=True):`,
          );
        })
        .with(P.nullish, () => {
          wn(`class ${node.name}(msgspec.Struct, omit_defaults=True):`);
        })
        .otherwise(() => {
          wn(
            `class ${node.name}(msgspec.Struct, kw_only=True, omit_defaults=True):`,
          );
        });
      if (node.description) {
        wn(`    """`);
        wn(`    ${node.description}`);
        wn(`    """`);
      }

      const sortedProperties = sortByRequired(node.properties);

      for (const { key, required, description, value } of sortedProperties) {
        w(`    ${key}: `);
        if (!required) w("Optional[");
        generateNode(value, writer);
        if (!required) w("] = None");
        wn("");
        if (description) {
          wn(`    """${description}"""`);
        }
      }
      wn("");
    })
    .with({ type: "descriminated-union" }, (node) => {
      const depWriter = new Writer();
      const { w: d, wn: dn } = depWriter.shorthand();
      const classes: string[] = [];
      w("Union[");
      for (const [name, properties] of Object.entries(node.members)) {
        for (const { value } of properties) {
          if (isComplexType(value)) {
            generateNode(value, depWriter);
          }
        }
        const className = `${cap(name)}${cap(node.name!)}`;
        classes.push(className);
        dn(
          `class ${className}(msgspec.Struct, tag_field="${node.descriminator}", tag="${name}"):`,
        );
        if (properties.length === 0) {
          dn("    pass");
        }

        const sortedProperties = sortByRequired(properties);

        for (const { key, required, description, value } of sortedProperties) {
          d(`    ${key}: `);
          if (!required) d("Optional[");
          !isComplexType(value)
            ? generateNode(value, depWriter)
            : d(value.name ?? value.type);
          if (!required) d("] = None");
          dn("");
          if (description) {
            dn(`    """${description}"""`);
          }
        }
        dn("");
      }
      w(classes.join(", "));
      writer.prepend(depWriter.output());
      wn("]");
    })
    .with({ type: "intersection" }, (node) => {
      assert(
        node.members.length === 2,
        "Intersection must have exactly 2 members",
      );
      assert(
        node.members[0]?.type === "object",
        "First member of intersection must be an object",
      );
      for (const member of node.members) {
        generateNode(member, writer);
      }
    })
    .with({ type: "unknown" }, () => {
      w("Any");
    })
    .exhaustive();
}

class Context {
  private static stack: Node[] = [];
  constructor(public readonly currentNode: Node) {
    Context.stack.push(this.currentNode);
  }

  get parent(): Node | undefined {
    return Context.stack.at(-2);
  }

  /**
   * When `n` is 1, this returns the parent.
   * When `n` is 2, this returns the grandparent.
   * etc.
   */
  getNthParent(n: number): Node | undefined {
    return Context.stack.at(-(n + 1));
  }

  closestName(): string | undefined {
    for (const node of [...Context.stack].reverse()) {
      // @ts-expect-error - We're looking for names on roots or declarations, this should be fine.
      const name = node.name || node.title;
      if (name) {
        return name;
      }
    }
    return undefined;
  }

  [Symbol.dispose]() {
    Context.stack = Context.stack.filter((n) => n !== this.currentNode);
  }
}

function cap(str: string): string {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function mapPythonType(type: string): string {
  return match(type)
    .with("string", () => "str")
    .with("number", () => "float")
    .with("integer", () => "int")
    .with("boolean", () => "bool")
    .otherwise(() => "Any");
}
