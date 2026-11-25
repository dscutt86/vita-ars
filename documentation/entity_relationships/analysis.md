# Entity Relationship Description

## Entities

### Sites
Each site is a location where VITA services are offered. They are unique locations, with a unique address and phone number. There are many sites.

### Schedule Blocks
Each block is a one-hour time period in a site's schedule. Each site can have many blocks, but each block belongs to only one site. Blocks for different sites may overlap in time and date. Blocks are unique, based on their date and time, and the site they belong to. I decided to use a unique 'id' value rather than a composite key, for ease of reference with the block appointments table. Each block has a capacity limit, which is normally 8 (BR08 and BR11), but may be changed when authorized by the site coordinator.

### Appointments
Each appointment represents the client and their information, and belongs to one block. There can be many blocks, and there can be many appointments, but there is only one block per appointment while there can be up to 8 appointments per block. We will use a bridge table between Appointments and Blocks as discussed below, but we will also store the id of the associated block. This is discussed further in the next section.

Another possible entity could be Clients, which would have a 1-to-many relationship with Appointments (1 client, many appointments). I have not shown this entity in my diagram as Appointments will do this work, representing the client. We will have no client login system, and there is no real need to store client data for the very long term.

### Block Appointments
A bridging table between Schedule Blocks and Appointments. It uses a composite key comprised of the related Block id and the Appointment id. This is potentially out of scope for the current project, but this simple inclusion helps us preserve information for future use and adds very little in terms of development time and overhead.


## Block Appointments Relationship

### Appointment Information Preservation Through Cancelations
There is a 1-to-many (8) relationship between Blocks and Appointments, and so we are not required to have a bridging table between them. However, I have decided that preserving appointment information, even after a cancelation, would be useful for later reference and even possible easy reinstatement. For this reason, I have decided to use a bridging table, Block Appointments, that is used as the authority when searching for appointments for a given site and block.

### Block Appointments as Authority
With the Block Appointments table acting as the authority for pulling valid appointments for each block, we are free to preserve appointment information for canceled (invalid) appointments. This also allows us to preserve generic block and appointment information (blocks and number of actual appointments for each block), while deleting customer information from the Appointments table, at such a time when it is deemed necessary to do so.

### Canceling an Appointment
To cancel an appointment, in the database, we simply delete the associated row for that appointment and block. Since the Block Appointments table acts as the authority, and not the Appointments table, and because we save the id of the associated Block in the Appointments table, we can easily search canceled appointments later without losing data or the Block-Appointment relationship.