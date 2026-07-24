type PlayerInfoProps = {
    name: string;
    elo: number | null;
    color: "white" | "black";
}

const PlayerInfo = ( { name, elo, color }: PlayerInfoProps ) => {
  return (
    <div className="player-info">
      <span className={`player-color ${color}`}></span>

       <div>
        <strong>{name || "Unknown Player"}</strong>
        <span>{elo != null ? ` (${elo})` : ""}</span>
      </div>
    </div>
  )
}

export default PlayerInfo;